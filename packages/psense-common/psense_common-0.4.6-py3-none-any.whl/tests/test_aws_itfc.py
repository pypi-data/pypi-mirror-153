import unittest
from unittest.mock import patch, Mock
from decimal import Decimal
from datetime import datetime, timedelta
import pytz
from psense_common.psense_aws_itfc import PSenseAWSInterface, is_float
import pandas as pd


class TestAWSItfc(unittest.TestCase):
    @patch("boto3.session.Session")
    def setUp(self, aws, test_mode=True):
        self.mock_table = Mock()
        self.mock_db = Mock()
        self.mock_db.Table.return_value = self.mock_table
        # self.mock_db.batch_write_item.return_value = dict()
        aws().resource.return_value = self.mock_db

        # generate a default response to Table methods
        self.mock_table.query.return_value = dict(
            Count=1, Items=[{"timestamp": datetime.utcnow().isoformat()}]
        )
        self.mock_table.put_item.return_value = dict()
        self.mock_table.delete_item.return_value = "{}"

        # generate a mock batch_writer(), attach it to mock_table.batch_writer()
        self.mock_batch_writer = Mock()
        self.mock_batch_writer.__enter__ = Mock(return_value=self.mock_batch_writer)
        self.mock_batch_writer.__exit__ = Mock(return_value=None)
        self.mock_table.batch_writer.return_value = self.mock_batch_writer

        self.aws = PSenseAWSInterface(testmode=test_mode, debugmode=True)
        self.test_expid = "19A01A001F01-0001-001-00-G01CPVX"

    def test_class_init(self):
        obj = PSenseAWSInterface(profile_name="doesnotexist")
        self.assertEqual(obj.aws.profile_name, "default")
        self.assertEqual(obj.aws.region_name, "us-east-1")
        self.assertEqual(obj.experiment_name, "")
        self.assertEqual(obj.experiment_info, [])
        self.assertFalse(obj.exp_is_valid)

    def test_is_float(self):
        self.assertTrue(is_float(1))
        self.assertTrue(is_float(0.5))
        self.assertTrue(is_float("0.5"))
        self.assertFalse(is_float("asdf"))
        self.assertFalse(is_float(pd.NA))
        self.assertFalse(is_float(datetime.now()))

    def test_set_query_config(self):
        self.aws.set_query_config(1, 2)
        self.assertEqual(self.aws.query_req_limit, 1)
        self.assertEqual(self.aws.query_req_count_limit, 2)

    def test_setget_expid(self):
        self.aws.set_experiment("asdf")
        self.assertEqual(self.aws.experiment_name, "asdf")
        self.assertEqual(self.aws.get_experiment(), "asdf")
        self.aws.set_experiment("")

    def test_verif_experiment(self):
        # experiment not verified if it is None
        self.assertFalse(self.aws.verif_experiment())

        # allow extended-length device ids
        self.aws.verif_experiment("19A01A001M9999-987A-654-3Z-213CCVACW")
        self.assertTrue(
            self.aws.verif_experiment("19A01A001M9999-987A-654-3Z-213CCVACW")
        )
        self.assertTrue(self.aws.exp_is_valid)

        # check parsing is done properly on verification
        self.assertTrue(self.aws.verif_experiment(self.test_expid))
        self.assertTrue(self.aws.exp_is_valid)
        self.assertEqual(self.aws.experiment_info["study"]["start"], "2019-01-01")
        self.assertEqual(self.aws.experiment_info["sensor"]["vsn"], "01")

        self.assertTrue(self.aws.verif_experiment("20H07R301M99-0400-400-00-G15CPVX"))
        self.assertTrue(self.aws.verif_experiment("20H07R301M99-0400-400-00-299OCWGRV"))

        self.assertTrue(self.aws.verif_experiment("20H07R301M99-0400-400-00-111GCV"))
        self.assertFalse(
            self.aws.verif_experiment("20H07R301M99-0400-400-00-115GCVGCV")
        )
        self.assertTrue(
            self.aws.verif_experiment("20H07R301M99-0400-400-00-315GCVGCVGCV")
        )
        self.assertFalse(
            self.aws.verif_experiment("20H07R301M99-0400-400-00-315GCVGCV")
        )

        self.assertTrue(self.aws.verif_experiment("20H07R301M99-9999-ABC-DE-215ACSCCB"))
        self.assertFalse(self.aws.verif_experiment("20H07R301M9-0400-400-00-215GCVGCV"))
        self.assertFalse(
            self.aws.verif_experiment("20H07R301M99-04000400-00-215GCVGCV")
        )
        self.assertFalse(self.aws.verif_experiment("20H07R301M99-0400-00-00-215GCVGCV"))

    # @patch('boto3.session.Session.resource')
    def test_check_experiment_data(self):
        self.setUp()  # reinitialize

        self.aws.test_mode = True
        valid, isactive, vout = self.aws.check_experiment_data("test")
        self.assertEqual(valid, "Yes")
        self.assertTrue(isactive)
        self.assertEqual(vout, -999)

        self.aws.test_mode = False
        self.mock_table.query.return_value = dict(
            Count=1, Items=[{"timestamp": datetime.utcnow().isoformat(), "vout1": 1}]
        )
        valid, isactive, vout = self.aws.check_experiment_data("test")
        self.assertEqual(valid, "Yes")
        self.assertTrue(isactive)
        self.assertEqual(vout, "1.000")

        self.mock_table.query.return_value = dict(
            Count=0,
            Items=[
                {
                    "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                    "vout1": 2,
                }
            ],
        )
        valid, isactive, vout = self.aws.check_experiment_data("test")
        self.assertEqual(valid, "No")
        self.assertFalse(isactive)
        self.assertEqual(vout, "0")

        self.mock_table.query.return_value = dict(
            Count=1,
            Items=[
                {
                    "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                    "vout1": 1,
                    "vout2": 2,
                    "vout3": 3,
                    "enable1": True,
                    "enable2": False,
                    "enable3": True,
                }
            ],
        )
        valid, isactive, vout = self.aws.check_experiment_data("test")
        self.assertEqual(vout, "1.000 / (off) / 3.000")

        self.aws.test_mode = True

    # @patch('boto3.session.Session.resource')
    def test_multiple_vouts_in_data(self):
        self.setUp()  # reinitialize

        self.aws.test_mode = False
        self.mock_table.query.return_value = dict(
            Count=1,
            Items=[
                {
                    "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                    "vout1": 0.5,
                    "vout2": 0.4999,
                    "vout3": 3,
                }
            ],
        )
        valid, isactive, vout = self.aws.check_experiment_data("test")
        self.assertEqual(valid, "Yes")
        self.assertFalse(isactive)
        self.assertEqual(vout, "0.500 / 0.500 / 3.000")

        # check that vout keys are sorted correctly
        self.mock_table.query.return_value = dict(
            Count=1,
            Items=[
                {
                    "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                    "vout3": 3,
                    "vout2": 2,
                    "vout1": 1,
                }
            ],
        )
        valid, isactive, vout = self.aws.check_experiment_data("test")
        self.assertEqual(valid, "Yes")
        self.assertFalse(isactive)
        self.assertEqual(vout, "1.000 / 2.000 / 3.000")
        self.aws.test_mode = True

    def test_aws_query_timeout(self):
        from botocore.exceptions import ReadTimeoutError

        self.setUp()
        self.aws.test_mode = False
        self.aws.verif_experiment(self.test_expid)

        # generate fake timeouts in response to a query
        self.mock_table.query.side_effect = ReadTimeoutError(
            endpoint_url="https://localhost"
        )

        # add_experiment() handled properly
        response, msg = self.aws.add_experiment()
        self.assertEqual(msg, "timeout")
        self.assertFalse(response)

        # check_experiment_data
        self.assertEqual(
            self.aws.check_experiment_data(self.test_expid), (None, None, None)
        )

        # get_event_data
        self.assertEqual(self.aws.get_event_data(), None)

        # get_sensordata_slice
        self.assertEqual(self.aws.get_sensordata_slice("2000", 1), (None, None))

        # get_sensordata_sincetimestamp
        self.assertEqual(self.aws.get_sensordata_sincetimestamp("2000"), (None, None))

        # get_sensor_data
        self.assertEqual(self.aws.get_sensor_data(), (None, None))

        # get_experiments
        self.mock_table.scan.return_value = dict(
            Count=0,
            Items=[],
        )
        self.assertEqual(self.aws.get_experiments(), [])

    def test_add_experiment(self):
        self.setUp()  # reinitialize
        # fail if no expid
        self.assertRaises(AssertionError, self.aws.add_experiment)
        self.aws.set_experiment(self.test_expid)
        # fail if expid has not been verified
        self.assertRaises(AssertionError, self.aws.add_experiment)
        self.aws.verif_experiment()

        # if in testmode, return true
        self.aws.test_mode = True
        res, msg = self.aws.add_experiment()
        self.assertTrue(res)

        # not in test mode, we need to mock the response
        self.aws.test_mode = False

        # handle aws success, but experiment already exists
        self.mock_table.query.return_value = dict(
            Count=1, Items=[{"timestamp": datetime.utcnow().isoformat()}]
        )
        res, msg = self.aws.add_experiment()
        self.assertFalse(res)
        self.assertEqual(msg, "exists")

        # handle aws success
        self.mock_table.query.return_value = dict(Count=0, Items=[])
        res, msg = self.aws.add_experiment()
        self.assertTrue(res)
        self.assertEqual(msg, "")

        # handle aws failed
        self.mock_table.put_item.side_effect = Exception("Test")
        res, msg = self.aws.add_experiment()
        self.assertFalse(res)
        self.assertEqual(msg, "error")

        self.aws.test_mode = True

    def test_add_sensordata(self):
        self.setUp()
        self.assertRaises(AssertionError, self.aws.add_sensordata)

        self.aws.verif_experiment(self.test_expid)

        self.aws.test_mode = True
        res = self.aws.add_sensordata(vout=[0], signal=[0])
        self.assertEqual(self.test_expid, res["experiment"])
        self.assertEqual(Decimal(0), res["signal1"])
        self.assertEqual(Decimal(0), res["vout1"])

        res = self.aws.add_sensordata(vout=0, signal=0, enable=1)
        self.assertEqual(self.test_expid, res["experiment"])
        self.assertEqual(Decimal(0), res["signal1"])
        self.assertEqual(Decimal(0), res["vout1"])
        self.assertTrue(res["enable1"])

        res = self.aws.add_sensordata(signal=[1, 2])
        self.assertEqual(Decimal(1), res["signal1"])
        self.assertEqual(Decimal(2), res["signal2"])
        self.assertEqual(Decimal(0.5), res["vout1"])
        self.assertEqual(Decimal(0.5), res["vout2"])

        # utcnow generates a naive timestamp, but we want to test w/ timezone info included
        entry_date = datetime.utcnow().replace(tzinfo=pytz.utc)
        res = self.aws.add_sensordata(timestamp=entry_date, vout=[0], signal=[0])
        self.assertEqual(entry_date.replace(tzinfo=None).isoformat(), res["timestamp"])
        self.assertEqual(Decimal(0), res["signal1"])
        self.assertEqual(Decimal(0), res["vout1"])

        entry_date = datetime.now()
        expected = (
            self.aws.local.localize(entry_date)
            .astimezone(pytz.utc)
            .replace(tzinfo=None)
            .isoformat()
        )
        res = self.aws.add_sensordata(timestamp=entry_date, vout=[0], signal=[0])
        self.assertEqual(expected, res["timestamp"])
        entry_date = entry_date.replace(tzinfo=None)
        res = self.aws.add_sensordata(timestamp=entry_date, vout=[0], signal=[0])
        self.assertEqual(expected, res["timestamp"])
        entry_date = datetime.now().isoformat("T")
        expected = (
            self.aws.local.localize(datetime.fromisoformat(entry_date))
            .astimezone(pytz.utc)
            .replace(tzinfo=None)
            .isoformat()
        )
        res = self.aws.add_sensordata(timestamp=entry_date, vout=[0], signal=[0])
        self.assertEqual(expected, res["timestamp"])

        self.aws.test_mode = False
        self.assertTrue(self.aws.add_sensordata(vout=[0], signal=[0]))
        self.mock_table.put_item.side_effect = Exception("Test")
        self.assertFalse(self.aws.add_sensordata(vout=[0], signal=[0]))
        self.aws.test_mode = True

    def test_generate_put_request(self):
        self.setUp()
        self.assertRaises(AssertionError, self.aws.generate_put_request, [])

        self.aws.verif_experiment(self.test_expid)
        check_timestamp = datetime.utcnow().isoformat()
        request = self.aws.generate_put_request([check_timestamp, 0.5, 0, True])
        self.assertEqual(request["experiment"], self.test_expid)
        self.assertEqual(request["vout1"], Decimal(0.5))
        self.assertEqual(request["signal1"], Decimal(0))
        self.assertTrue(request["enable1"])

        # try multi-channel data
        test_data = [check_timestamp, 0.5, 0, False, 1.5, 1, True]
        request = self.aws.generate_put_request(test_data)
        self.assertEqual(request["experiment"], self.test_expid)
        self.assertEqual(request["timestamp"], check_timestamp)
        self.assertEqual(request["vout1"], Decimal(0.5))
        self.assertEqual(request["signal1"], Decimal(0))
        self.assertFalse(request["enable1"])
        self.assertEqual(request["vout2"], Decimal(1.5))
        self.assertEqual(request["signal2"], Decimal(1))
        self.assertTrue(request["enable2"])

    @patch("time.sleep", return_value=None)
    def test_add_bulk_sensordata(self, delay=None):
        self.setUp()
        self.assertRaises(AssertionError, self.aws.add_bulk_sensordata, [])

        self.aws.verif_experiment(self.test_expid)

        data = [
            [datetime.utcnow().isoformat(), 1, 0.1, True],
            [datetime.utcnow(), 2, 0.2, True],
            [datetime.now(), 3, 0.3, True],
        ]

        self.aws.test_mode = True
        self.assertTrue(self.aws.add_bulk_sensordata(data))
        self.aws.batch_request_limit = 1

        extradata = [[datetime.now(), 3, 0.3, True] for i in range(26)]
        self.assertTrue(self.aws.add_bulk_sensordata(extradata))

        self.aws.test_mode = False
        self.mock_batch_writer._response = dict(
            ResponseMetadata=dict(HTTPStatusCode=200)
        )
        self.assertTrue(self.aws.add_bulk_sensordata(data))
        self.assertTrue(self.aws.add_bulk_sensordata(extradata))

        self.mock_batch_writer._response = dict(
            ResponseMetadata=dict(HTTPStatusCode=301, RetryAttempts=1),
            UnprocessedItems=dict(),
        )
        self.assertFalse(self.aws.add_bulk_sensordata(extradata))
        self.mock_batch_writer.put_item.side_effect = Exception("Test")

    def test_get_experiments(self):
        self.setUp()
        self.mock_table.scan.return_value = dict(
            Count=2,
            Items=[{"experiment": "Experiment1"}, {"experiment": "Experiment2"}],
        )
        ret = self.aws.get_experiments()
        "return a list of experiment ids"
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(ret[0], "Experiment1")
        self.assertEqual(ret[1], "Experiment2")

        "experiments should be sorted"
        self.mock_table.scan.return_value = dict(
            Count=2,
            Items=[{"experiment": "Experiment2"}, {"experiment": "Experiment1"}],
        )
        ret = self.aws.get_experiments()
        self.assertEqual(ret[0], "Experiment1")
        self.assertEqual(ret[1], "Experiment2")

        "scan may not return everything if size > 1MB"
        self.aws.query_req_count_limit = 2
        self.mock_table.scan.return_value = dict(
            Count=2,
            Items=[{"experiment": "Experiment2"}, {"experiment": "Experiment1"}],
            LastEvaluatedKey="Experiment1",
        )
        ret = self.aws.get_experiments()
        # KLUDGE: only return unique experiments, so in this case we only get 2
        self.assertEqual(len(ret), 2)

    def test_get_sensor_data(self):
        self.setUp()
        self.aws.verif_experiment(self.test_expid)
        check_timestamp = datetime.utcnow()
        count, request = self.aws.get_sensor_data()
        self.assertEqual(count, 1)
        self.assertEqual(request["signal1"][0], 10)
        self.assertEqual(request["vout1"][0], 0.4)

        self.aws.test_mode = False
        self.mock_table.query.return_value = {
            "Count": 1,
            "Items": [
                {
                    "experiment": self.test_expid,
                    "timestamp": check_timestamp.isoformat("T"),
                    "signal1": 20,
                    "vout1": 0.4,
                    "enable1": True,
                }
            ],
        }
        count, request = self.aws.get_sensor_data()

        self.assertEqual(count, 1)
        self.assertEqual(request["signal1"][0], 20)
        self.assertEqual(request["vout1"][0], 0.4)
        self.assertTrue(request["enable1"][0])

        self.aws.set_query_config(req_size=2, req_count=1)
        self.mock_table.query.return_value = {
            "Count": 2,
            "Items": [
                {
                    "experiment": self.test_expid,
                    "timestamp": (check_timestamp - timedelta(minutes=10)).isoformat(
                        "T"
                    ),
                    "signal1": 20,
                    "vout1": 0.4,
                    "enable1": True,
                }
            ]
            * 2,
        }
        count, request = self.aws.get_sensor_data()
        self.assertEqual(count, 2)
        self.assertEqual(request["signal1"][0], 20)
        self.assertEqual(request["vout1"][0], 0.4)
        self.assertTrue(request["enable1"][0])

        self.aws.set_query_config(req_size=2, req_count=2)
        count, request = self.aws.get_sensor_data()
        self.assertEqual(count, 4)
        self.assertEqual(request["signal1"][0], 20)
        self.assertEqual(request["vout1"][0], 0.4)
        self.assertTrue(request["enable1"][0])

        self.aws.set_query_config(req_size=2, req_count=3)
        self.mock_table.query.side_effect = [
            {
                "Count": 2,
                "Items": [
                    {
                        "experiment": self.test_expid,
                        "timestamp": (
                            check_timestamp - timedelta(minutes=10)
                        ).isoformat("T"),
                        "signal1": 10,
                        "vout1": 0.4,
                        "enable1": True,
                    }
                ]
                * 2,
            },
            {
                "Count": 2,
                "Items": [
                    {
                        "experiment": self.test_expid,
                        "timestamp": (
                            check_timestamp - timedelta(minutes=10)
                        ).isoformat("T"),
                        "signal1": 10,
                        "vout1": 0.4,
                        "enable1": True,
                    }
                ]
                * 2,
            },
            {
                "Count": 1,
                "Items": [
                    {
                        "experiment": self.test_expid,
                        "timestamp": (
                            check_timestamp - timedelta(minutes=10)
                        ).isoformat("T"),
                        "signal1": 5,
                        "vout1": 0.1,
                        "enable1": False,
                    }
                ],
            },
        ]
        count, request = self.aws.get_sensor_data()
        self.assertEqual(count, 5)
        self.assertEqual(request["signal1"][0], 10)
        self.assertEqual(request["vout1"][0], 0.4)
        self.assertTrue(request["enable1"][0])

        self.assertEqual(request["signal1"][-1], 5)
        self.assertEqual(request["vout1"][-1], 0.1)
        self.assertFalse(request["enable1"][-1])

        self.aws.test_mode = True

    def test_get_sensor_data_multianalyte(self):
        self.setUp()
        self.aws.verif_experiment(self.test_expid)
        self.aws.test_mode = False
        self.mock_table.query.return_value = {
            "Count": 1,
            "Items": [
                {
                    "experiment": self.test_expid,
                    "timestamp": (datetime.utcnow() - timedelta(minutes=10)).isoformat(
                        "T"
                    ),
                    "signal1": 10,
                    "vout1": 0.4,
                    "enable1": True,
                    "signal2": 20,
                    "vout2": 0.6,
                    "enable2": True,
                    "signal3": -30,
                    "vout3": -0.5,
                    "enable3": False,
                }
            ],
        }
        count, request = self.aws.get_sensor_data()
        self.aws.test_mode = True

        self.assertEqual(count, 1)
        self.assertEqual(request["signal1"][0], 10)
        self.assertEqual(request["signal2"][0], 20)
        self.assertEqual(request["signal3"][0], -30)

        self.assertEqual(request["vout1"][0], 0.4)
        self.assertEqual(request["vout2"][0], 0.6)
        self.assertEqual(request["vout3"][0], -0.5)

        self.assertTrue(request["enable1"][0])
        self.assertTrue(request["enable2"][0])
        self.assertFalse(request["enable3"][0])

    def test_get_sensordata_slice(self):
        self.setUp()
        self.aws.verif_experiment(self.test_expid)
        check_timestamp = datetime.utcnow()

        self.aws.test_mode = True
        count, request = self.aws.get_sensordata_slice(
            check_timestamp.isoformat("T"), 5
        )
        self.assertEqual(count, 1)
        self.assertEqual(request["signal1"][0], 5)
        self.assertEqual(request["vout1"][0], 0.2)
        self.assertTrue(request["enable1"][0])

        self.aws.test_mode = False
        self.mock_table.query.return_value = {
            "Count": 1,
            "Items": [
                {
                    "experiment": self.test_expid,
                    "timestamp": (check_timestamp - timedelta(minutes=10)).isoformat(
                        "T"
                    ),
                    "signal1": 6,
                    "vout1": 0.3,
                    "enable1": True,
                }
            ],
        }
        count, request = self.aws.get_sensordata_slice(check_timestamp, 5)
        self.assertEqual(count, 1)
        self.assertEqual(request["signal1"][0], 6)
        self.assertEqual(request["vout1"][0], 0.3)

        self.mock_table.query.return_value = {
            "Count": 3,
            "Items": [
                {
                    "experiment": self.test_expid,
                    "timestamp": (check_timestamp - timedelta(minutes=10)).isoformat(
                        "T"
                    ),
                    "signal1": 10,
                    "vout1": 0.4,
                    "enable1": True,
                }
            ]
            * 3,
        }
        count, request = self.aws.get_sensordata_slice(check_timestamp, 5)
        self.assertEqual(count, 3)

        self.mock_table.query.return_value = {"Count": 0, "Items": []}
        count, request = self.aws.get_sensordata_slice(check_timestamp, 5)
        self.assertEqual(count, 0)

        self.aws.test_mode = True

    def test_get_event_data(self):
        self.setUp()
        self.aws.set_experiment(self.test_expid)
        self.assertRaises(AssertionError, self.aws.get_event_data)
        self.aws.verif_experiment()

        self.aws.test_mode = True
        self.assertEqual(len(self.aws.get_event_data()), 1)

    def test_add_event(self):
        self.setUp()
        self.aws.set_experiment(self.test_expid)
        self.assertRaises(AssertionError, self.aws.add_event, 0, "", "", 0)
        self.aws.verif_experiment()
        self.assertRaises(
            AssertionError, self.aws.add_event, 0, "", "not-a-real-type", 0
        )

        self.aws.test_mode = True
        self.assertTrue(self.aws.add_event(0, datetime.now(), "Lactate", 0))
        self.assertTrue(
            self.aws.add_event(0, datetime.utcnow().isoformat(), "Lactate", 0)
        )

    def test_delete_event(self):
        self.setUp()
        self.aws.set_experiment(self.test_expid)
        self.assertRaises(AssertionError, self.aws.delete_event, 0, "", "")
        self.aws.verif_experiment()
        self.assertRaises(
            AssertionError, self.aws.delete_event, 0, "", "not-a-real-type"
        )
        self.aws.test_mode = True
        self.assertTrue(self.aws.delete_event(0, datetime.now(), "Lactate"))
        self.assertTrue(
            self.aws.delete_event(0, datetime.utcnow().isoformat(), "Lactate")
        )
        self.aws.test_mode = False
        self.assertEqual(self.aws.delete_event(0, datetime.now(), "Lactate"), dict())
        self.aws.test_mode = True


if __name__ == "__main__":
    unittest.main()
