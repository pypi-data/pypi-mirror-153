import time
import pytz
from datetime import datetime, timedelta
import pandas as pd

# dynamodb
import boto3
from botocore.client import Config
from botocore.exceptions import ReadTimeoutError
from boto3.dynamodb.conditions import Key, Attr
from dynamodb_json import json_util
from decimal import Decimal
import logging
import types

# percusense
from psense_common import psense_format

valid_types = [
    "Glucose",
    "Lactate",
    "Oxygen",
    "Ketone",
    "Temperature",
    "Multianalyte",
    "Choline",
    "Acetylcholine",
    "Interferent",
    "Injection",
]

# logging
log = logging.getLogger()


""" functions """


def is_float(val):
    "check if the input value is a floating point number"
    try:
        # if this isn't a numeric value, we'll cause a valueerror exception
        float(val)
        # don't allow NaN values, either.
        if pd.isnull(val):
            return False
        return True
    except BaseException:
        return False


# override the _flush() method of Table.batch_writer(). This modification just persists the response from AWS to self._response
def _flush(self):
    items_to_send = self._items_buffer[: self._flush_amount]
    self._items_buffer = self._items_buffer[self._flush_amount :]
    self._response = self._client.batch_write_item(
        RequestItems={self._table_name: items_to_send}
    )
    unprocessed_items = self._response["UnprocessedItems"]

    if unprocessed_items and unprocessed_items[self._table_name]:
        # Any unprocessed_items are immediately added to the
        # next batch we send.
        self._items_buffer.extend(unprocessed_items[self._table_name])
    else:
        self._items_buffer = []

    log.debug(
        "Batch write sent %s, unprocessed: %s",
        len(items_to_send),
        len(self._items_buffer),
    )


""" classes """

LOG_PREFIX = "PSenseAWSInterface"


class PSenseAWSInterface(object):
    def __init__(
        self,
        profile_name: str = "pshield",
        debugmode: bool = False,
        testmode: bool = False,
    ):
        self.debug = debugmode
        self.test_mode = testmode
        self.batch_req_limit = 25
        self.batch_req_cooldown_secs = 10
        self.query_req_limit = 5000
        self.query_req_count_limit = 2

        self.local = pytz.timezone("America/Los_Angeles")
        self.vset = {
            "default": 0,
            "Glucose": 0.5,
            "Lactate": 0.5,
            "Oxygen": -0.5,
            "Ketone": -0.2,
        }
        self.we_count = 1

        # initialize DynamoDB connection
        config = Config(connect_timeout=5, read_timeout=5, retries={"max_attempts": 0})
        try:
            self.aws = boto3.session.Session(profile_name=profile_name)
        except BaseException:
            # profile doesn't exist
            log.debug(
                f"{LOG_PREFIX}.__init__: failed to load profile: {profile_name}. Loading defaults"
            )
            self.aws = boto3.session.Session(region_name="us-east-1")

        self.db = self.aws.resource("dynamodb", config=config)
        self.table_experiments = self.db.Table("Experiments")
        self.table_sensordata = self.db.Table("SensorData")
        self.table_eventdata = self.db.Table("CalibrationData")

        # check for validity
        self.pf = psense_format.psense_exp_title()

        # initialize experiment information
        self.experiment_name = ""
        self.experiment_info = []
        self.exp_is_valid = False

    def set_query_config(self, req_size: int = 5000, req_count: int = 2):
        """change dynamodb query parameters based on size:
        req_size: maximum number of items to return
        req_count: number of queries to allow (total = req_size*req_count)
        """
        self.query_req_limit = req_size
        self.query_req_count_limit = req_count
        log.debug(
            f"{LOG_PREFIX}.set_query_config: limits -- count={req_count} size={req_size}"
        )

    def get_experiment(self):
        "return the experiment id"
        return self.experiment_name

    def set_experiment(self, experiment_name: str):
        "update the experiment id"
        self.experiment_name = experiment_name

    def verif_experiment(self, experiment_name: str = ""):
        "return whether the experiment id follows the psense naming convention"
        if len(experiment_name) > 0:
            self.set_experiment(experiment_name)

        experiment_name = self.get_experiment()
        self.experiment_info = self.pf.decode(experiment_name)

        try:
            # invalid experiment name, or missing data
            # assert len(experiment_name) == 32
            assert isinstance(self.experiment_info, dict)
            assert isinstance(self.experiment_info["study"], dict)
            assert isinstance(self.experiment_info["sensor"], dict)

            assert self.experiment_info["study"]["type"]
            assert self.experiment_info["study"]["run"].isnumeric()
            assert len(self.experiment_info["study"]["device"]) > 2

            sensor_code = self.experiment_info["sensor"]["code"].split("-")
            assert len(sensor_code) == 3
            assert len(sensor_code[0]) == 4
            assert len(sensor_code[1]) == 3
            assert len(sensor_code[2]) == 2

            assert len(self.experiment_info["sensor"]["vsn"]) == 2  # 2-digit vsn

            assert isinstance(self.experiment_info["sensor"]["electrodes"], list)
            we_count = self.experiment_info["sensor"]["count"]
            if we_count.isnumeric():
                assert len(self.experiment_info["sensor"]["electrodes"]) == int(
                    we_count
                )
                assert len(experiment_name) == 25 + len(
                    self.experiment_info["study"]["device"]
                ) + 3 * int(
                    we_count
                )  # three letters per electrode, no more or less
            else:
                assert len(self.experiment_info["sensor"]["electrodes"]) == 1
                assert len(experiment_name) == 29 + len(
                    self.experiment_info["study"]["device"]
                )  # 32 letters in the old experiment id format

            assert isinstance(self.experiment_info["sensor"]["electrodes"][0], dict)

        except BaseException as E:
            log.info(
                f"{LOG_PREFIX}.verif_experiment: {experiment_name} is invalid ({E})"
            )
            self.exp_is_valid = False
            return False

        log.info(f"{LOG_PREFIX}.verif_experiment: {experiment_name} is valid")
        self.exp_is_valid = True
        return True

    def check_experiment_data(
        self, experiment_name: str, active_threshold_seconds: int = 5400
    ):
        "return whether an experiment exists and has data"
        log.debug(
            f"{LOG_PREFIX}.check_experiment_data: Checking for items associated with {experiment_name}"
        )

        if self.test_mode:
            return ("Yes", True, -999)

        res = "No"
        is_active = False
        last_vout = "0"

        if len(experiment_name) > 0:  # skip if there is no data
            try:
                response = self.table_sensordata.query(
                    KeyConditionExpression=Key("experiment").eq(experiment_name),
                    Limit=1,  # +return a single data point
                    ScanIndexForward=False,  # +return the most recent value
                )
            except ReadTimeoutError:
                log.error(
                    f"{LOG_PREFIX}.check_experiment_data: failed. Timeout on query for experiment={experiment_name}"
                )
                return (None, None, None)

            if response["Count"] > 0:
                res = "Yes"
                last_received = (
                    datetime.utcnow()
                    - datetime.fromisoformat(response["Items"][0]["timestamp"][:19])
                ).total_seconds()
                is_active = last_received < active_threshold_seconds

                last_enable = [
                    value
                    for key, value in sorted(response["Items"][0].items())
                    if "enable" in key
                ]
                last_vout = [
                    value
                    for key, value in sorted(response["Items"][0].items())
                    if "vout" in key
                ]
                if len(last_enable):  # are there enable flags in the data?
                    last_vout = " / ".join(
                        [
                            "{:.3f}".format(last_vout[i]) if enabled else "(off)"
                            for i, enabled in enumerate(last_enable)
                        ]
                    )
                else:
                    last_vout = " / ".join(map("{:.3f}".format, last_vout))

        return (res, is_active, last_vout)

    def add_experiment(
        self, device_version: str = "unknown", sample_period: int = 30, vset=None
    ):
        "Push experiment id to the Experiments table"
        expid = self.get_experiment()
        assert self.exp_is_valid, f"Experiment [{expid}] has not been validated"

        if self.test_mode:
            response = dict(Items=[])
        else:
            try:
                response = self.table_experiments.query(
                    KeyConditionExpression=Key("experiment").eq(
                        expid
                    ),  # check for a single experiment id
                    Limit=1,  # +return a single data point
                )
            except ReadTimeoutError:
                log.error(
                    f"{LOG_PREFIX}.add_experiment: op failed. Timeout on query for experiment={expid}"
                )
                return False, "timeout"

        if vset is None:
            vset = self.vset.get(
                self.experiment_info["sensor"]["electrodes"][0]["type"],
                self.vset["default"],
            )

        if len(response["Items"]) > 0:
            log.error(
                f"{LOG_PREFIX}.add_experiment: op failed. {expid} already exists."
            )
            return False, "exists"
        else:
            item = {
                "experiment": expid,
                "t_start": datetime.utcnow().isoformat(),
                "auto_creation": 1,
                "dev_id": "{}".format(self.experiment_info["study"]["device"]),
                "dev_ver": device_version,
                "we_count": "{}".format(self.we_count),
                "we_types": self.experiment_info["sensor"]["electrodes"],
                "v_out": "{}".format(vset),
                "t_samp": "{}".format(sample_period),
            }
            if not self.test_mode:
                try:
                    self.table_experiments.put_item(Item=item)
                except BaseException as E:
                    log.error(
                        f"{LOG_PREFIX}.add_experiment: op failed. {expid} could not be added ({E})"
                    )
                    return False, "error"

        log.info(
            f"{LOG_PREFIX}.add_experiment: op succeeded. {expid} added to dynamodb table"
        )
        return True, ""

    def add_sensordata(self, timestamp=[], vout=None, signal: list = [0], enable=True):
        "Push (time,vout,isig,enable) tuple to the SensorData table"
        assert (
            self.exp_is_valid
        ), f"Experiment [{self.get_experiment()}] has not been validated"

        if isinstance(timestamp, datetime):
            if timestamp.tzinfo is None:
                timestamp = self.local.localize(timestamp).astimezone(pytz.utc)
            else:
                timestamp = timestamp.astimezone(pytz.utc)
        elif isinstance(timestamp, str):
            timestamp = self.local.localize(
                datetime.fromisoformat(timestamp)
            ).astimezone(pytz.utc)
        else:
            timestamp = datetime.utcnow()

        if vout is None:
            vout = [
                self.vset.get(
                    self.experiment_info["sensor"]["electrodes"][0]["type"],
                    self.vset["default"],
                )
            ] * len(signal)

        if is_float(signal):
            signal = [signal]
        if is_float(vout):
            vout = [vout] * len(signal)
        if is_float(enable):
            enable = [enable] * len(signal)

        item = {
            "experiment": self.get_experiment(),
            # timestamps are UTC. THe web app plots it is in pacific
            "timestamp": timestamp.replace(tzinfo=None).isoformat(),
        }
        for i in range(len(signal)):
            item["signal{}".format(i + 1)] = Decimal(
                str(round(signal[i], 2))
            )  # floats -> Decimal for ddb
            item["vout{}".format(i + 1)] = Decimal(
                str(round(vout[i], 3))
            )  # floats -> Decimal for ddb
            item["enable{}".format(i + 1)] = enable[i]  # booleans are supported in ddb

        if self.test_mode:
            log.info(f"{LOG_PREFIX}.add_sensordata: test mode put_item successful")
            return item

        try:
            self.table_sensordata.put_item(Item=item)
            log.info(
                f"{LOG_PREFIX}.add_sensordata: sensor data put_item was successful"
            )
        except BaseException:
            log.error(
                f"{LOG_PREFIX}.add_sensordata: sensor data put_item failed. {item}"
            )
            return False

        return True

    def generate_put_request(self, row):
        "helper function for batch writing sensor data"
        assert (
            self.exp_is_valid
        ), f"Experiment [{self.get_experiment()}] has not been validated"

        # extract signals from the provided row
        request = {
            "experiment": self.get_experiment(),
            "timestamp": row[0],
        }
        for i in range(int((len(row) - 1) / 3)):
            request["signal{}".format(i + 1)] = Decimal(str(round(row[3 * i + 2], 2)))
            request["vout{}".format(i + 1)] = Decimal(str(round(row[3 * i + 1], 3)))
            request["enable{}".format(i + 1)] = row[3 * i + 3]

        # build the request dict
        return request

    def add_bulk_sensordata(self, data):
        assert (
            self.exp_is_valid
        ), f"Experiment [{self.get_experiment()}] has not been validated"

        log.info(
            f"{LOG_PREFIX}.add_bulk_sensordata: batch writing {len(data)} records to SensorData"
        )

        requests = []
        for sample in data:
            timestamp = sample[0]
            if isinstance(timestamp, str):
                timestamp = pytz.utc.localize(
                    datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
                )
            elif isinstance(timestamp, pd.Timestamp):
                timestamp = self.local.localize(timestamp.to_pydatetime()).astimezone(
                    pytz.utc
                )
            else:
                timestamp = (timestamp).astimezone(pytz.utc)

            sample[0] = timestamp.replace(tzinfo=None).isoformat()
            requests.append(self.generate_put_request(sample))

            if len(requests) >= self.batch_req_limit:
                log.debug(
                    f"{LOG_PREFIX}.add_bulk_sensordata: inserting batch of [25] records into [SensorData]"
                )

                if not self.test_mode:
                    with self.table_sensordata.batch_writer(
                        overwrite_by_pkeys=["experiment", "timestamp"]
                    ) as batch:
                        batch._flush = types.MethodType(_flush, batch)
                        for request in requests:
                            batch.put_item(Item=request)

                    res = batch._response
                    if res["ResponseMetadata"].get("HTTPStatusCode", None) != 200:
                        res = batch._response
                        log.warning(
                            "{}.add_bulk_sensordata: batch_writer() returned unexpected response: [RequestId] {} [Status] {} [RetryAttempts] {} [Unprocessed] {}".format(
                                LOG_PREFIX,
                                res["ResponseMetadata"].get("RequestId", None),
                                res["ResponseMetadata"].get("HTTPStatusCode", None),
                                res["ResponseMetadata"].get("RetryAttempts", None),
                                res.get("UnprocessedItems", None),
                            )
                        )
                        log.warning(
                            f"{LOG_PREFIX}.add_bulk_sensordata: batch_writer() batch = {requests}"
                        )
                        return False

                    time.sleep(self.batch_req_cooldown_secs)

                requests = []

        if not self.test_mode and len(requests) > 0:
            log.debug(
                f"{LOG_PREFIX}.add_bulk_sensordata: inserting batch of [{len(requests)}] records into [SensorData]"
            )

            with self.table_sensordata.batch_writer(
                overwrite_by_pkeys=["experiment", "timestamp"]
            ) as batch:
                batch._flush = types.MethodType(_flush, batch)
                for request in requests:
                    batch.put_item(Item=request)

            res = batch._response
            if res["ResponseMetadata"].get("HTTPStatusCode", None) != 200:
                log.warning(
                    "{}add_bulk_sensordata: batch_writer() returned unexpected response: [RequestId] {} [Status] {} [RetryAttempts] {} [Unprocessed] {}".format(
                        LOG_PREFIX,
                        res["ResponseMetadata"].get("RequestId", None),
                        res["ResponseMetadata"].get("HTTPStatusCode", None),
                        res["ResponseMetadata"].get("RetryAttempts", None),
                        res.get("UnprocessedItems", None),
                    )
                )
                log.warning(
                    f"{LOG_PREFIX}.add_bulk_sensordata: batch_writer() batch = {requests}"
                )
                return False

        return True

    def get_experiments(self):
        "request entire list of sensor experiments from aws. WARNING: boto3 scan operation is expensive"
        try:
            response = self.table_experiments.scan()
            data = response["Items"]
        except ReadTimeoutError:
            log.error(
                f"{LOG_PREFIX}.get_experiments: request failed. Timeout when querying the experiments table"
            )
            return []

        num_scans_executed = 1
        while (
            "LastEvaluatedKey" in response
            and num_scans_executed < self.query_req_count_limit
        ):
            try:
                response = self.table_experiments.scan(
                    ExclusiveStartKey=response["LastEvaluatedKey"]
                )
                data.extend(response["Items"])
                num_scans_executed += 1
            except ReadTimeoutError:
                log.error(
                    f"{LOG_PREFIX}.get_experiments: request failed. Timeout when querying the experiments table"
                )
                return []

        experiments = set()
        for exp in data:
            experiments.add(exp["experiment"])

        log.debug(
            f"{LOG_PREFIX}.get_experiments: request returned {len(experiments)} unique experiment ids"
        )
        return list(sorted(experiments))

    def get_sensor_data(self):
        "request sensor data from aws"
        expid = self.get_experiment()
        assert self.exp_is_valid, f"Experiment [{expid}] has not been validated"

        if self.test_mode:
            res = {
                "Count": 1,
                "Items": [
                    {
                        "experiment": expid,
                        "timestamp": (
                            datetime.utcnow() - timedelta(minutes=10)
                        ).isoformat("T"),
                        "signal1": 10,
                        "vout1": 0.4,
                        "enable1": True,
                    }
                ],
            }
        else:
            try:
                res = self.table_sensordata.query(
                    KeyConditionExpression=Key("experiment").eq(expid),
                    Limit=self.query_req_limit,
                )
            except ReadTimeoutError:
                log.error(
                    f"{LOG_PREFIX}.get_sensor_data: request failed. Timeout on query for experiment={expid}"
                )
                return None, None

        count, res = self.aws_to_df(res)
        log.info(
            f"{LOG_PREFIX}.get_sensor_data: {expid} initial request found {count} records"
        )

        more_to_retrieve = count == self.query_req_limit
        num_queries_executed = 1
        while more_to_retrieve and num_queries_executed < self.query_req_count_limit:
            last_received_timestamp = datetime.isoformat(res.index[-1])
            q_count, q_res = self.get_sensordata_sincetimestamp(
                last_received_timestamp, num_queries_executed
            )
            res = pd.concat([res, q_res], axis=0, join="outer")
            count += q_count

            num_queries_executed += 1
            more_to_retrieve = q_count % self.query_req_limit == 0

        log.info(f"{LOG_PREFIX}.get_sensor_data: {expid} found {count} records")

        return count, res

    def get_sensordata_sincetimestamp(self, last_received_timestamp, query_count=0):
        expid = self.get_experiment()
        assert self.exp_is_valid, f"Experiment [{expid}] has not been validated"

        log.info(
            f"{LOG_PREFIX}.get_sensordata_sincetimestamp: {expid} [count={query_count}] (start={last_received_timestamp})"
        )

        if self.test_mode:
            res = {
                "Count": 1,
                "Items": [
                    {
                        "experiment": expid,
                        "timestamp": (
                            datetime.utcnow() - timedelta(minutes=10)
                        ).isoformat("T"),
                        "signal1": 10,
                        "vout1": 0.4,
                        "enable1": True,
                    }
                ],
            }
        else:
            try:
                res = self.table_sensordata.query(
                    KeyConditionExpression=Key("experiment").eq(expid)
                    & Key("timestamp").gt(last_received_timestamp),
                    Limit=self.query_req_limit,
                )
            except ReadTimeoutError:
                log.error(
                    f"{LOG_PREFIX}.get_sensordata_sincetimestamp: query failed. Timeout on query for experiment={expid}"
                )
                return None, None

        count, res = self.aws_to_df(res)

        query_count += 1
        log.debug(
            f"{LOG_PREFIX}.get_sensordata_sincetimestamp: {expid} returned {count} items"
        )

        # recursively query for more data based on last timestamp
        if count == self.query_req_limit and query_count < self.query_req_count_limit:
            last_received_timestamp = datetime.isoformat(res.index[-1])

            q_count, q_result = self.get_sensordata_sincetimestamp(
                last_received_timestamp, query_count
            )

            res = pd.concat([res, q_result], axis=0, join="outer")
            count += q_count

        return count, res

    def get_sensordata_slice(self, timestamp_start, samples):
        "get x samples of data starting from a specific timestamp"
        expid = self.get_experiment()
        assert self.exp_is_valid, f"Experiment [{expid}] has not been validated"

        if self.test_mode:
            res = {
                "Count": 1,
                "Items": [
                    {
                        "experiment": expid,
                        "timestamp": (
                            datetime.utcnow() - timedelta(minutes=10)
                        ).isoformat("T"),
                        "signal1": 5,
                        "vout1": 0.2,
                        "enable1": True,
                    }
                ],
            }
        else:
            try:
                res = self.table_sensordata.query(
                    KeyConditionExpression=Key("experiment").eq(expid)
                    & Key("timestamp").gt(timestamp_start),
                    Limit=samples,
                )
            except ReadTimeoutError:
                log.error(
                    f"{LOG_PREFIX}.get_sensordata_slice: request failed. Timeout on query for experiment={expid}"
                )
                return None, None

        count, res = self.aws_to_df(res)

        log.debug(
            f"{LOG_PREFIX}.get_sensordata_slice: {expid} ({timestamp_start}) returned {count} items"
        )
        return count, res

    def aws_to_df(self, response):
        "convert a aws response to a pandas dataframe, indexed by timestamp"

        data = json_util.loads(response)
        records = data["Items"]
        count: int = data["Count"]

        res: pd.DataFrame = pd.json_normalize(records)
        if count > 0:  # only attempt modification if there are records
            res.drop(columns="experiment", inplace=True)
            try:
                res["timestamp"] = pd.to_datetime(res["timestamp"])
            except BaseException:
                pass

            try:
                res["timestamp"] = res["timestamp"].apply(
                    lambda x: x.replace(microsecond=0)
                )  # trim microseconds
            except BaseException:
                pass
            res.set_index("timestamp", inplace=True)

        return count, res

    def get_event_data(self):
        expid = self.get_experiment()
        assert self.exp_is_valid, f"Experiment [{expid}] has not been validated"

        if self.test_mode:
            res = {
                "Count": 1,
                "Items": [
                    {
                        "experiment": expid,
                        "timestamp": "1|{}".format(
                            (datetime.utcnow() - timedelta(minutes=10)).isoformat("T")
                        ),
                        "reference": 100,
                        "type": "Glucose",
                    }
                ],
            }
        else:
            try:
                res = self.table_eventdata.query(
                    KeyConditionExpression=Key("experiment").eq(expid)
                )
            except ReadTimeoutError:
                log.error(
                    f"{LOG_PREFIX}.get_event_data: query failed. Timeout on query for experiment={expid}"
                )
                return None

        data = json_util.loads(res)
        records = data["Items"]
        count = data["Count"]

        res = pd.json_normalize(records)
        res["set"] = res["timestamp"].map(lambda a: a.split("|")[0])
        res["timestamp"] = res["timestamp"].map(lambda a: a.split("|")[1])
        log.debug(f"{LOG_PREFIX}.get_event_data: found {count} items")

        return res

    def add_event(self, set: int, timestamp: str, type: str, reference: float):
        expid = self.get_experiment()
        assert self.exp_is_valid, f"Experiment [{expid}] has not been validated"
        assert type in valid_types, f"Type [{type}] is not valid"

        try:
            dt = pytz.utc.localize(datetime.fromisoformat(timestamp))
        except BaseException:
            dt = timestamp.astimezone(pytz.utc)

        log.debug(f"{LOG_PREFIX}.add_event: insert @ {dt.isoformat()}")
        newitem = {
            "experiment": expid,
            "timestamp": f"{set}|{dt.replace(tzinfo=None).isoformat()}",
            "type": type,
            "reference": Decimal(str(reference)),
        }

        if self.test_mode:
            return True

        try:
            self.table_eventdata.put_item(Item=newitem)
            log.info(f"{LOG_PREFIX}.add_event: event data put_item was successful")
        except BaseException:
            log.error(f"{LOG_PREFIX}.add_event: event data put_item failed. {newitem}")
            return False

        return True

    def delete_event(self, set: int, timestamp: str, type: str):
        expid = self.get_experiment()
        assert self.exp_is_valid, f"Experiment [{expid}] has not been validated"
        assert type in valid_types, f"Type [{type}] is not valid"
        try:
            dt = pytz.utc.localize(datetime.fromisoformat(timestamp))
        except BaseException:
            dt = timestamp.astimezone(pytz.utc)

        log.debug(
            f"{LOG_PREFIX}.delete_event: {expid} ({dt.replace(tzinfo=None).isoformat()}, {type}, {set})"
        )

        if self.test_mode:
            return True

        response = self.table_eventdata.delete_item(
            Key={
                "experiment": expid,
                "timestamp": f"{set}|{dt.replace(tzinfo=None).isoformat()}",
            }
        )
        response = json_util.loads(response)
        return response
