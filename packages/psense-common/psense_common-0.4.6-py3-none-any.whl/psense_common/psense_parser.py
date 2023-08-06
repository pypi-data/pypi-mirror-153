import re
import pandas as pd
import numpy as np
import os
import pytz
from datetime import datetime

# import collections
import json

# logging
import logging

log = logging.getLogger()


def is_float(val):
    try:
        # if this isn't a numeric value, we'll cause a valueerror exception
        float(val)
        return True
    except BaseException:
        return False


""" classes """


class SensorDataFormat:
    def __init__(
        self,
        name=None,
        delimiter=",",
        has_timestamp=True,
        columns=None,
        type_is_sensor=None,
    ):
        self.name = name
        self.delimiter = delimiter
        self.type_is_sensor = type_is_sensor
        self.has_timestamp = has_timestamp
        self.columns = dict(
            type=None,
            timestamp=None,
            vref=None,
            enable1=None,
            vout1=None,
            vref1=None,
            discard1=None,
            signal1=None,
            enable2=None,
            vout2=None,
            vref2=None,
            discard2=None,
            signal2=None,
            enable3=None,
            vout3=None,
            vref3=None,
            discard3=None,
            signal3=None,
        )
        if columns and isinstance(columns, dict):
            for key in list(columns.keys()):
                self.columns[key] = columns[key]

    def set_key(self, key, value):
        self.columns[key] = value

    def get_key(self, key):
        return self.columns.get(key, None)

    def get_header(self, key):
        data = self.get_key(key)
        if data:
            return data[0]
        else:
            return None

    def get_index(self, key):
        data = self.get_key(key)
        if data:
            return data[1]
        else:
            return None

    def data_keys(self):
        keys = [None] * 30
        for key in list(self.columns.keys()):
            val = self.get_key(key)
            if val:
                keys[val[1]] = key

        return list(filter(None, keys))

    def data_headers(self):
        header_names = [None] * 30
        for key in list(self.columns.keys()):
            val = self.get_key(key)
            if val:
                header_names[val[1]] = val[0]

        return list(filter(None, header_names))

    def data_indices(self):
        header_index = []
        for key in list(self.columns.keys()):
            val = self.get_key(key)
            if val:
                header_index.append(val[1])

        return header_index


DEV_B03_SENSOR = SensorDataFormat(
    name="DEV-B03-SENSOR",
    delimiter=",",
    columns=dict(
        timestamp=("timestamp", 0),
        enable1=("enable_w1", 4),
        enable2=("enable_w2", 8),
        enable3=("enable_w3", 12),
        vref=("v_cr", 3),
        vout1=("v_w1", 7),
        vout2=("v_w2", 11),
        vout3=("v_w3", 15),
        signal1=("i_w1", 6),
        signal2=("i_w2", 10),
        signal3=("i_w3", 14),
        discard1=("discard_w1", 5),
        discard2=("discard_w2", 9),
        discard3=("discard_w3", 13),
    ),
)

DEV_B03_AGGREG = SensorDataFormat(
    name="DEV-B03-AGGREG",
    delimiter=",",
    columns=dict(
        timestamp=("timestamp", 1),
        type=("type", 2),
        enable1=("enable_w1", 7),
        enable2=("enable_w2", 11),
        enable3=("enable_w3", 15),
        vref=("v_cr", 6),
        vout1=("v_w1", 10),
        vout2=("v_w2", 14),
        vout3=("v_w3", 18),
        signal1=("i_w1", 9),
        signal2=("i_w2", 13),
        signal3=("i_w3", 17),
        discard1=("discard_w1", 8),
        discard2=("discard_w2", 12),
        discard3=("discard_w3", 16),
    ),
    type_is_sensor="SENSOR",
)

DEV_B04_SENSOR = SensorDataFormat(
    name="DEV-B04-SENSOR",
    delimiter=",",
    columns=dict(
        timestamp=("timestamp", 0),
        enable1=("enable_w1", 4),
        enable2=("enable_w2", 8),
        enable3=("enable_w3", 12),
        vref1=("v_c1", 3),
        vref3=("v_c3", 14),
        vout1=("v_w1", 7),
        vout2=("v_w2", 11),
        vout3=("v_w3", 15),
        signal1=("i_w1", 6),
        signal2=("i_w2", 10),
        signal3=("i_w3", 14),
        discard1=("discard_w1", 5),
        discard2=("discard_w2", 9),
        discard3=("discard_w3", 13),
    ),
)

DEV_B04_AGGREG = SensorDataFormat(
    name="DEV-B04-AGGREG",
    delimiter=",",
    columns=dict(
        timestamp=("timestamp", 1),
        type=("type", 2),
        enable1=("enable_w1", 7),
        enable2=("enable_w2", 11),
        enable3=("enable_w3", 15),
        vref1=("v_c1", 6),
        vref3=("v_c3", 19),
        vout1=("v_w1", 10),
        vout2=("v_w2", 14),
        vout3=("v_w3", 18),
        signal1=("i_w1", 9),
        signal2=("i_w2", 13),
        signal3=("i_w3", 17),
        discard1=("discard_w1", 8),
        discard2=("discard_w2", 12),
        discard3=("discard_w3", 16),
    ),
    type_is_sensor="SENSOR",
)

DEV_S01_AGGREG = SensorDataFormat(
    name="DEV-S01-AGGREG",
    delimiter=",",
    columns=dict(
        timestamp=("timestamp", 1),
        type=("type", 2),
        enable1=("enable_w1", 7),
        enable2=("enable_w2", 12),
        vout1=("vw_w1", 10),
        vout2=("vw_w2", 15),
        vref1=("vc_w1", 11),
        vref2=("vc_w2", 16),
        signal1=("i_w1", 9),
        signal2=("i_w2", 14),
        discard1=("discard_w1", 8),
        discard2=("discard_w2", 13),
    ),
    type_is_sensor="SENSOR",
)

DEV_S01_SENSOR = SensorDataFormat(
    name="DEV-S01-SENSOR",
    delimiter=",",
    columns=dict(
        timestamp=("timestamp", 0),
        enable1=("enable_w1", 4),
        enable2=("enable_w2", 9),
        vout1=("vw_w1", 7),
        vout2=("vw_w2", 12),
        vref1=("vc_w1", 8),
        vref2=("vc_w2", 13),
        signal1=("i_w1", 6),
        signal2=("i_w2", 11),
        discard1=("discard_w1", 5),
        discard2=("discard_w2", 10),
    ),
)

DEV_STREAM_V1 = SensorDataFormat(
    name="BWII-STREAM",
    delimiter=",",
    columns=dict(
        timestamp=("Timestamp", 0),
        vout1=("Vout1", 1),
        signal1=("Signal1", 2),
        vout2=("Vout2", 3),
        signal2=("Signal2", 4),
        vout3=("Vout3", 5),
        signal3=("Signal3", 6),
    ),
)

DEV_STREAM_V2 = SensorDataFormat(
    name="DEV-STREAM",
    delimiter=",",
    columns=dict(
        timestamp=("Timestamp", 0),
        enable1=("Enable1", 1),
        vout1=("Vout1", 2),
        signal1=("Signal1", 3),
        enable2=("Enable2", 4),
        vout2=("Vout2", 5),
        signal2=("Signal2", 6),
        enable3=("Enable3", 7),
        vout3=("Vout3", 8),
        signal3=("Signal3", 9),
    ),
)

BWII_S01_SENSOR = SensorDataFormat(
    name="BWII-S01-ECHEM",
    delimiter=",",
    columns=dict(
        timestamp=("DATETIME", 0),
        type=("sensor_record", 1),
        enable1=("SEN1_ON", 6),
        enable2=("SEN2_ON", 11),
        vref1=("VC1", 5),
        vref2=("VC2", 10),
        vout1=("VW1", 4),
        vout2=("VW2", 9),
        signal1=("I1", 3),
        signal2=("I2", 8),
        discard1=("DISC1", 7),
        discard2=("DISC2", 12),
    ),
    type_is_sensor="sensor_record",
)

BWII_S01_IMPEDANCE = SensorDataFormat(
    name="BWII-S01-ZDATA",
    delimiter=",",
    columns=dict(
        timestamp=("DATETIME", 1),
        type=("Z_sensor_record", 2),
        vout1=("Vac", 3),
        vout2=("Vdc", 4),
        signal1=("Freq", 5),
        signal2=("Mag", 6),
        signal3=("Phase", 7),
        enable1=("SENZ_ON", 8),
        discard1=("DISC_Z", 9),
    ),
    type_is_sensor="Z_sensor_record",
)

BWII_B04 = SensorDataFormat(
    name="BWII-B04",
    delimiter=",",
    columns=dict(
        timestamp=("DATETIME", 0),
        type=("trace_record", 1),
        enable1=("SEN1_ON", 6),
        enable2=("SEN2_ON", 10),
        enable3=("SEN3_ON", 15),
        vref1=("VC1", 5),
        vref3=("VC2", 14),
        vout1=("VW1", 4),
        vout2=("VW2", 9),
        vout3=("VW3", 13),
        signal1=("I1", 3),
        signal2=("I2", 8),
        signal3=("I3", 12),
        discard1=("DISC1", 7),
        discard2=("DISC2", 11),
        discard3=("DISC3", 16),
    ),
    type_is_sensor="sensor_record",
)

BWII_B03 = SensorDataFormat(
    name="BWII-B03",
    delimiter=",",
    columns=dict(
        timestamp=("DATETIME", 0),
        type=("trace_record", 1),
        enable1=("SEN1_ON", 6),
        enable2=("SEN2_ON", 10),
        enable3=("SEN3_ON", 14),
        vref=("VC", 5),
        vout1=("VW1", 4),
        vout2=("VW2", 9),
        vout3=("VW3", 13),
        signal1=("I1", 3),
        signal2=("I2", 8),
        signal3=("I3", 12),
        discard1=("DISC1", 7),
        discard2=("DISC2", 11),
        discard3=("DISC3", 15),
    ),
    type_is_sensor="sensor_record",
)

BWII_B02 = SensorDataFormat(
    name="BWII-B02",
    delimiter=",",
    columns=dict(
        timestamp=("DATETIME", 0),
        type=("trace_record", 1),
        enable1=("SEN1_ON", 7),
        enable2=("SEN2_ON", 13),
        vref1=("VR1", 5),
        vref2=("VR2", 11),
        vout1=("VW1", 4),
        vout2=("VW2", 10),
        signal1=("I1", 3),
        signal2=("I2", 9),
        discard1=("DISC1", 8),
        discard2=("DISC2", 14),
    ),
    type_is_sensor="sensor_record",
)

WEB_APP = SensorDataFormat(
    name="WEB-APP",
    delimiter=",",
    columns=dict(
        timestamp=("timestamp", 0),
        signal1=("Raw1", 1),
        vout1=("Vout1", 2),
        signal2=("Raw2", 3),
        vout2=("Vout2", 4),
        signal3=("Raw3", 5),
        vout3=("Vout3", 6),
    ),
)

PSHIELD = SensorDataFormat(
    name="PSHIELD",
    delimiter=",",
    has_timestamp=False,
    columns=dict(timestamp=("Elapsed Seconds", 1), signal1=("Current(nA)", 2)),
)

VFP600 = SensorDataFormat(
    name="VFP",
    delimiter="\t",
    has_timestamp=False,
    columns=dict(vout1=("V", 0), signal1=("A", 1)),
)

CHI = SensorDataFormat(
    name="CHI",
    delimiter=",",
    has_timestamp=False,
    columns=dict(
        timestamp=("Time/s", 0),
        signal1=("i1/A", 1),
        signal2=("i2/A", 2),
        signal3=("i3/A", 3),
        signal4=("i4/A", 4),
        signal5=("i5/A", 5),
        signal6=("i6/A", 6),
        signal7=("i7/A", 7),
        signal8=("i8/A", 8),
    ),
)


class PSenseParser:
    def __init__(self, filename="", exp_config=None, debugmode=False):
        self.debugmode = debugmode
        self.valid_types = [
            "BWII-B02",
            "BWII-B03",
            "BWII-B04",
            "BWII-S01-ECHEM",
            "BWII-S01-ZDATA",
            "BWII-STREAM",
            "DEV-B03-SENSOR",
            "DEV-B03-AGGREG",
            "DEV-B04-SENSOR",
            "DEV-B04-AGGREG",
            "DEV-S01-SENSOR",
            "DEV-S01-AGGREG",
            "DEV-STREAM",
            "WEB-APP",
            "PSHIELD",
            "VFP",
            "EXPLAIN",
            "CHI",
            "RAWCSV",  # special case
        ]

        self.source_formats = {
            "BWII-B02": BWII_B02,
            "BWII-B03": BWII_B03,
            "BWII-B04": BWII_B04,
            "BWII-S01-ECHEM": BWII_S01_SENSOR,
            "BWII-S01-ZDATA": BWII_S01_IMPEDANCE,
            "BWII-STREAM": DEV_STREAM_V1,
            "DEV-B03-SENSOR": DEV_B03_SENSOR,
            "DEV-B03-AGGREG": DEV_B03_AGGREG,
            "DEV-B04-SENSOR": DEV_B04_SENSOR,
            "DEV-B04-AGGREG": DEV_B04_AGGREG,
            "DEV-S01-SENSOR": DEV_S01_SENSOR,
            "DEV-S01-AGGREG": DEV_S01_AGGREG,
            "DEV-STREAM": DEV_STREAM_V2,
            "WEB-APP": WEB_APP,
            "PSHIELD": PSHIELD,
            "VFP": VFP600,
            "EXPLAIN": None,
            "CHI": CHI,
            "RAWCSV": None,
        }

        self.file_identifier = {
            "BWII-B02": "DATETIME,trace_record,rNUM,I1,VW1,VR1,VC1,SEN1_ON,DISC1,I2,VW2,VR2,VC2,SEN2_ON,DISC2,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT",
            "BWII-B03": "DATETIME,trace_record,rNUM,I1,VW1,VC,SEN1_ON,DISC1,I2,VW2,SEN2_ON,DISC2,I3,VW3,SEN3_ON,DISC3,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT",
            "BWII-B04": "DATETIME,trace_record,rNUM,I1,VW1,VC1,SEN1_ON,DISC1,I2,VW2,SEN2_ON,DISC2,I3,VW3,VC2,SEN3_ON,DISC3,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT",
            "BWII-S01-ECHEM": "DATETIME,sensor_record,rNUM,I1,VW1,VC1,SEN1_ON,DISC1,I2,VW2,VC2,SEN2_ON,DISC2,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT",
            "BWII-S01-ZDATA": "DATETIME,Z_sensor_record,ZrNUM,VAC,VDC,FREQ,MAG,PHASE,SENZ_ON,DISC_Z,,,,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT",
            "BWII-STREAM": "BWIIData,",
            "DEV-B03-SENSOR": "timestamp,id,v_batt,v_cr,enable_w",
            "DEV-B03-AGGREG": "index,timestamp,type,event,id,v_batt,v_cr,enable_w1,discard_w1,i_w1,v_w1,enable_w2,discard_w2,i_w2,v_w2,enable_w3,discard_w3,i_w3,v_w3",
            "DEV-B04-SENSOR": "timestamp,id,v_batt,v_c1,enable_w1,discard_w1,i_w1,v_w1,enable_w2,discard_w2,i_w2,v_w2,enable_w3,discard_w3,i_w3,v_w3,v_c3",
            "DEV-B04-AGGREG": "index,timestamp,type,event,id,v_batt,v_c1,enable_w1,discard_w1,i_w1,v_w1,enable_w2,discard_w2,i_w2,v_w2,enable_w3,discard_w3,i_w3,v_w3,v_c3",
            "DEV-S01-SENSOR": "timestamp,id,v_batt,temp,enable_w",
            "DEV-S01-AGGREG": "index,timestamp,type,event,id,v_batt,temp,enable_w1,discard_w1,i_w1,vw_w1,vc_w1,enable_w2,discard_w2,i_w2,vw_w2,vc_w2",
            "DEV-STREAM": "psense-dev-controller,",
            "WEB-APP": "AppSettings",
            "PSHIELD": "PotentiostatShield",
            "VFP": "VFP600",
            "EXPLAIN": "EXPLAIN",
            "CHI": "Amperometrici-tCurve",
            "RAWCSV": "timestamp,enable1,discard1,signal1,vout1,",
        }

        self.header_text = {
            "BWII-B02": "DATETIME,trace_record,rNUM,I1,VW1,VR1,VC1,SEN1_ON,DISC1,I2,VW2,VR2,VC2,SEN2_ON,DISC2,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT",
            "BWII-B03": "DATETIME,trace_record,rNUM,I1,VW1,VC,SEN1_ON,DISC1,I2,VW2,SEN2_ON,DISC2,I3,VW3,SEN3_ON,DISC3,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT",
            "BWII-B04": "DATETIME,trace_record,rNUM,I1,VW1,VC1,SEN1_ON,DISC1,I2,VW2,SEN2_ON,DISC2,I3,VW3,VC2,SEN3_ON,DISC3,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT",
            "BWII-S01-ECHEM": "DATETIME,sensor_record,rNUM,I1,VW1,VC1,SEN1_ON,DISC1,I2,VW2,VC2,SEN2_ON,DISC2,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT",
            "BWII-S01-ZDATA": "DATETIME,Z_sensor_record,ZrNUM,VAC,VDC,FREQ,MAG,PHASE,SENZ_ON,DISC_Z,,,,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT",
            "BWII-STREAM": "Timestamp,Vout1,Signal1,Vout2,Signal2",
            "DEV-B03-SENSOR": "timestamp,id,v_batt,v_cr,enable_w",
            "DEV-B03-AGGREG": "index,timestamp,type,event,id,v_batt,v_cr,enable_w",
            "DEV-B04-SENSOR": "timestamp,id,v_batt,v_c1,enable_w1,discard_w1,i_w1,v_w1,enable_w2,discard_w2,i_w2,v_w2,enable_w3,discard_w3,i_w3,v_w3,v_c3",
            "DEV-B04-AGGREG": "index,timestamp,type,event,id,v_batt,v_c1,enable_w1,discard_w1,i_w1,v_w1,enable_w2,discard_w2,i_w2,v_w2,enable_w3,discard_w3,i_w3,v_w3,v_c3",
            "DEV-S01-SENSOR": "timestamp,id,v_batt,temp,enable_w",
            "DEV-S01-AGGREG": "index,timestamp,type,event,id,v_batt,temp,enable_w",
            "DEV-STREAM": "Timestamp,Enable1,Vout1,Signal1,Enable2,Vout2,Signal2",
            "WEB-APP": "timestamp,Raw",
            "PSHIELD": "SampleCount,ElapsedSeconds,Current",
            "VFP": "VA",
            "EXPLAIN": "PtTVf",
            "CHI": "Time/s,i1/A",
            "RAWCSV": "timestamp,enable1,discard1,signal1,vout1,",
        }

        # what's the current offset between local and UTC?
        # assumes things are collected in PST/PDT
        self.local = pytz.timezone("America/Los_Angeles")
        self.time_offset = datetime.now(self.local).utcoffset()

        self.source = None
        self.data = None
        self.name = filename
        self.config = exp_config
        self.vout = None

    def force_source(self, source):
        "hard-code the input file-format (alt. to identify_file_source)"
        if source is None or source in self.valid_types:
            log.debug("forcing source to be type [{}]".format(source))
            self.source = source
        else:
            raise IOError(
                "Invalid source ({}). Must be in list: {}".format(
                    source, self.valid_types
                )
            )

    def identify_file_source(self, fpath=""):
        "read the file header to identify the file format"
        for cur in self.valid_types:
            if self.find_header_text(fpath, self.file_identifier[cur]):
                log.debug("file [{}] has source [{}]".format(fpath, cur))
                self.source = cur
                return cur

        log.warning("file [{}] has no known source".format(fpath))
        self.source = None
        return None

    def read_variable_header_file(self, fname, line, **kwargs):
        "helper function returns data in the form of tuple of (data, header)"
        header_text = ""
        with open(fname, "r", encoding="utf8", errors="ignore") as f:
            pos = -1
            stripped = ""
            while not stripped.startswith(line):
                if f.tell() == pos:
                    break
                pos = f.tell()
                cur_line = f.readline().strip()
                stripped = re.sub(r"\s", "", cur_line)
                header_text += cur_line

            f.seek(pos)
            if pos == os.path.getsize(fname):
                log.warning("unable to extract header: eof")
                return None, None

            log.debug("header extracted (len={})".format(pos))
            return pd.read_csv(f, **kwargs), header_text

    def process_record(self, data_format, row, num_channels=None):
        row = row.split(data_format.delimiter)
        keys = data_format.data_keys()

        # if the row data type doesn't match our parser, skip processing and return None
        check_sensor = data_format.type_is_sensor
        if check_sensor and row[data_format.get_index("type")] != check_sensor:
            return [None] * 4

        if len(keys) > len(row):
            keys = [key for key in keys if data_format.get_index(key) < len(row)]

        if "timestamp" in keys:
            timestamp = row[data_format.get_index("timestamp")]
        else:
            timestamp = (datetime.utcnow() + self.time_offset).isoformat("T")

        # signal
        signals = [
            float(row[data_format.get_index(key)])
            for key in keys
            if key.startswith("signal")
        ]

        # voltage
        voltages = [col for col in keys if col.startswith("vout")]
        vout = []
        for index, v in enumerate(voltages):
            vref = "vref{}".format(v[-1])
            if vref in keys:
                vout.append(
                    float(row[data_format.get_index(v)])
                    - float(row[data_format.get_index(vref)])
                )
            elif "vref" in keys:
                vout.append(
                    float(row[data_format.get_index(v)])
                    - float(row[data_format.get_index("vref")])
                )
            elif "vref1" in keys:
                vout.append(
                    float(row[data_format.get_index(v)])
                    - float(row[data_format.get_index("vref1")])
                )
            else:
                vout.append(float(row[data_format.get_index(v)]))

        if len(vout) == 0:
            vout = [None] * len(signals)

        # enable
        enable = [
            bool(float(row[data_format.get_index(key)]))
            for key in keys
            if key.startswith("enable")
        ]
        if len(enable) == 0:
            enable = [True] * len(signals)

        elts = min(
            num_channels if num_channels else len(signals), len(vout), len(enable)
        )

        return [timestamp, vout[:elts], signals[:elts], enable[:elts]]

    def data_format(self):
        return self.source_formats[self.source]

    def parse_record(self, row, num_channels=None):
        "parse a single sensor data record assuming the detected file format"

        dataformat = self.source_formats[self.source]
        [timestamp, vout, isig, enable] = self.process_record(
            dataformat, row, num_channels
        )

        if timestamp is None:
            return None

        # custom modifications for specific source types
        if self.source == "VFP":
            isig = [i * 1e9 for i in isig]
        elif self.source == "PSHIELD":
            timestamp = datetime.utcfromtimestamp(float(timestamp))
            offset = timestamp.astimezone(self.local).utcoffset()
            timestamp = (timestamp + offset).isoformat("T")
        elif self.source == "WEB-APP":
            timestamp = timestamp.replace(" ", "T")

        # data formats with invalid/missing time. For real-time purposes, just use the current time.
        if self.source in (
            "BWII-B02",
            "BWII-B03",
            "BWII-B04",
            "BWII-S01-ECHEM",
            "BWII-S01-ZDATA",
            "DEV-B03-SENSOR",
            "DEV-B03-AGGREG",
            "DEV-S01-SENSOR",
            "DEV-S01-AGGREG",
            "CHI",
        ):
            timestamp = (datetime.utcnow() + self.time_offset).isoformat("T")

        if self.source in ("BWII-B02", "BWII-B03", "BWII-B04", "BWII-S01-ECHEM"):
            vout = [v / 1000 for v in vout]

        if vout is None and self.vout is not None:
            vout = self.vout

        log.debug(
            "[PSenseParser][parse_record] data: {}".format([timestamp, vout, isig])
        )
        return [timestamp, vout, isig, enable]

    def update_props(self, data, period=None, vout=None):
        self.data = data

        if period is None and "timestamp" in list(data.columns):
            period = data["timestamp"].diff().median()
        self.period = period

        if vout is None:
            vout = data["vout1"].median()
        self.vout = vout

    def process_download(
        self, data_format, fname, origin_timestamp, origin_is_end, skiprows=0
    ):
        self.data = None

        data, header = self.read_variable_header_file(
            fname,
            self.header_text[self.source],
            sep=data_format.delimiter,
            skiprows=skiprows,
        )

        # data validation: get rid of extra whitespace (\t)
        data.columns = [name.strip() for name in list(data.columns)]
        data = data.apply(
            lambda x: x.astype("str").str.strip() if x.dtype == "object" else x
        )

        # some formats have variable # of columns (e.g. 2-WE vs 3-WE). Reduce the expected headers/keys as necessary
        raw_headers = data_format.data_headers()
        raw_keys = data_format.data_keys()
        keep_index = [
            index
            for index, header in enumerate(raw_headers)
            if header in list(data.columns)
        ]
        if len(keep_index) < len(raw_headers):
            raw_headers = [raw_headers[index] for index in keep_index]
            raw_keys = [raw_keys[index] for index in keep_index]

        data = data[
            raw_headers
        ]  # drop df columns that aren't defined in the data format
        data.columns = (
            raw_keys  # rename df columns to match our standard data format keys
        )
        # data validation: ensure only numbers where we expect them..
        columns = [
            col
            for col in raw_keys
            if col.startswith("vout")
            or col.startswith("signal")
            or col.startswith("vref")
        ]
        mask = data[columns].applymap(is_float).all(1)
        data = data[mask]
        data[columns] = data[columns].apply(pd.to_numeric, errors="coerce")

        # drop nan-only columns
        data.dropna(axis=1, how="all", inplace=True)
        raw_keys = (
            data.columns
        )  # update valid raw_keys to remove any keys that have been dropped from the data

        # if possible, filter data to ONLY those records that contain sensor data
        if "type" in raw_keys and data_format.type_is_sensor:
            mask = (
                data[["type"]]
                .applymap(lambda str: str == data_format.type_is_sensor)
                .all(1)
            )
            data = data[mask]
            data.drop(columns="type", inplace=True)

        # compute vout value
        voltages = [col for col in raw_keys if col.startswith("vout")]
        for v in voltages:
            vref = "vref{}".format(v[-1])
            if vref in raw_keys:
                data[v] = (data[v] - data[vref]) / 1000
            elif "vref" in raw_keys:
                data[v] = (data[v] - data["vref"]) / 1000
            elif "vref1" in raw_keys:
                data[v] = (data[v] - data["vref1"]) / 1000

        refs = [col for col in raw_keys if col.startswith("vref")]
        data.drop(columns=refs, inplace=True)

        # enable and discard flags should be boolean
        make_boolean = [
            flag
            for flag in raw_keys
            if flag.startswith("enable") or flag.startswith("discard")
        ]
        data[make_boolean] = data[make_boolean].applymap(
            lambda x: bool(float(x)) if is_float(x) else x.lower().strip() == "true"
        )
        if len(make_boolean) > 0:
            for col in make_boolean:
                data[col] = data[col].astype("bool")
        else:
            for col in range(
                len([col for col in raw_keys if col.startswith("signal")])
            ):
                data["enable{}".format(col + 1)] = True

        # process timestamps if there is a timestamp entry
        if "timestamp" in raw_keys and data_format.has_timestamp:
            # shift timestamps if required (user selection)
            if origin_timestamp is not None:
                origin_timestamp = pd.Timestamp(origin_timestamp)
                if "timestamp" in raw_keys:
                    data["timestamp"] = pd.to_datetime(
                        data["timestamp"], errors="coerce"
                    )
                    if origin_is_end:
                        time_offset = origin_timestamp - data["timestamp"].iloc[-1]
                    else:
                        time_offset = origin_timestamp - data["timestamp"].iloc[0]

                    data["timestamp"] = data["timestamp"] + time_offset
            else:
                data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")

            # drop duplicated rows (based on timestamp)
            data.drop_duplicates(subset="timestamp", keep="first", inplace=True)

            # drop corrupted timestamps
            mask = (
                data[["timestamp"]]
                .applymap(lambda cell: isinstance(cell, pd.Timestamp))
                .all(1)
            )
            data = data[mask]

        self.update_props(
            data=data,
            vout=[data[col].median() for col in raw_keys if col.startswith("vout")],
        )

        return data, header

    def load_rawfile(self, fname, origin_timestamp, origin_is_end):
        """parse an entire sensor flat-file into pandas DataFrame.
        Different logic is implemented depending on the file format."""
        self.data = None

        log.debug(
            "[PSenseParser][load_rawfile] {}".format(
                [fname, origin_timestamp, origin_is_end]
            )
        )

        if self.source in [
            "BWII-B02",
            "BWII-B03",
            "BWII-B04",
            "BWII-S01-ECHEM",
            "BWII-STREAM",
            "DEV-B03-SENSOR",
            "DEV-B03-AGGREG",
            "DEV-B04-SENSOR",
            "DEV-B04-AGGREG",
            "DEV-S01-SENSOR",
            "DEV-S01-AGGREG",
            "DEV-STREAM",
            "WEB-APP",
        ]:
            data_format = self.source_formats[self.source]
            self.process_download(data_format, fname, origin_timestamp, origin_is_end)
            return True
        elif self.source == "RAWCSV":
            data = pd.read_csv(fname, parse_dates=["timestamp"], index_col=False)

            # remove unnamed columns (typically, occurs if the file had an index column)
            data.drop(
                [col for col in data.columns if "Unnamed" in col], axis=1, inplace=True
            )
            # data.set_index("timestamp", inplace=True)
            self.update_props(data=data, vout=0)
            return True

        elif self.source == "PSHIELD":
            data, header = self.process_download(
                PSHIELD, fname, origin_timestamp, origin_is_end, skiprows=[1]
            )
            v_out = float(
                re.search(r"Output Voltage:([\W\.0-9]+)", header).group()[15:]
            )
            data["vout1"] = np.ones(len(data.index)) * v_out
            data["timestamp"] = (
                pd.to_datetime(self.data["timestamp"], unit="s")
                .dt.tz_localize("utc")
                .dt.tz_convert(self.local)
                .dt.tz_localize(None)
            )
            self.update_props(
                data=data[["timestamp", "vout1", "signal1", "enable1"]], vout=v_out
            )
            return True

        elif self.source == "VFP":
            assert (
                origin_timestamp is not None
            ), "\terror: this file type requires a timestamp to be specified"
            data, header = self.process_download(
                VFP600, fname, origin_timestamp, origin_is_end, skiprows=[1]
            )

            period = 1 / float(
                re.search(r"FREQ\tQUANT\t([0-9-\.E]+)", header).group()[11:]
            )
            origin_timestamp = pd.Timestamp(origin_timestamp).to_pydatetime()
            if origin_is_end:
                origin_timestamp -= pd.Timedelta(seconds=(len(data.index) - 1) * period)

            data["timestamp"] = pd.to_datetime(
                np.asarray(data.index) * period, unit="s", origin=origin_timestamp
            )
            data.columns = ["vout1", "signal1", "enable1", "timestamp"]
            data = data[["timestamp", "vout1", "signal1", "enable1"]]
            # convert from scientific notation string to floats
            data["signal1"] = data["signal1"].astype(np.float64) * 1e9
            self.update_props(data=data, vout=data["vout1"].median(), period=period)
            return True

        elif self.source == "EXPLAIN":

            data, header = self.read_variable_header_file(
                fname,
                "PtTVf",
                sep="\t",
                skiprows=[1],
                usecols=lambda x: x.upper() in ["T", "VF", "IM"],
            )

            # extract starting time
            date_start = re.search(r"DATE\tLABEL\t([\-\./0-9]+)", header).group()[11:]
            time_start = re.search(r"TIME\tLABEL\t([\.0-9:]+)", header).group()[11:]
            origin_timestamp = datetime.strptime(
                date_start + "T" + time_start, "%m/%d/%YT%H:%M:%S"
            )

            # remove corrupted data
            mask = data.applymap(is_float).all(1)
            data = data[mask]

            # rearrange and add columns
            data.columns = ["timestamp", "vout1", "signal1"]

            # adjust from seconds elapsed to PST
            data["timestamp"] = pd.to_datetime(
                round(data["timestamp"]), unit="s", origin=origin_timestamp
            )

            # convert from A to nA
            data["signal1"] = data["signal1"].astype(np.float64) * 1e9
            # spoof the enable flag
            data["enable1"] = np.ones(len(data.index), dtype=bool)

            # save
            self.update_props(data=data, vout=data["vout1"].median())
            return True

        elif self.source == "CHI":
            data, header = self.process_download(
                CHI, fname, origin_timestamp, origin_is_end, skiprows=[1]
            )

            channels = len(re.findall(r"Channel [0-9]+", header))
            # Vset, only shown for Chan 1. Assume all channels set the same(?)
            for chan in range(channels):
                if chan == 0:
                    v_out = [
                        float(
                            re.search(r"Init E \(V\) = ([\-\.0-9]+)", header).group()[
                                13:
                            ]
                        )
                    ]
                else:
                    v_out.append(
                        float(
                            re.search(
                                r"E{} = ([\-\.0-9]+)".format(chan + 1), header
                            ).group()[5:]
                        )
                    )

            # Sampling period
            period = int(
                re.search(r"Sample Interval \(s\) = ([\.0-9]+)", header).group()[22:]
            )

            # Extract Finish Time from Header
            timestamp = (header[: re.search("Amperometric", header).span()[0]]).strip()
            origin_timestamp = datetime.strptime(timestamp, "%B %d, %Y   %H:%M:%S")
            origin_timestamp -= pd.Timedelta(seconds=(len(data.index)) * period)

            # rearrange and add columns
            columns = ["timestamp"]
            for chan in range(channels):
                columns.append("signal{}".format(chan + 1))
            for chan in range(channels):
                columns.append("enable{}".format(chan + 1))

            data.columns = columns

            columns = ["timestamp"]
            for chan in range(channels):
                data["vout{}".format(chan + 1)] = np.ones(len(data.index)) * v_out[chan]
                data["signal{}".format(chan + 1)] = (
                    data["signal{}".format(chan + 1)].astype(np.float64) * 1e9
                )
                columns.extend(
                    [
                        "vout{}".format(chan + 1),
                        "signal{}".format(chan + 1),
                        "enable{}".format(chan + 1),
                    ]
                )

            # adjust from seconds elapsed to PST
            data["timestamp"] = pd.to_datetime(
                round(data["timestamp"]), unit="s", origin=origin_timestamp
            )

            # save
            self.update_props(data=pd.DataFrame(data, columns=columns), vout=v_out)
            return True

        else:
            raise ValueError("Input file {name} not recognized.".format(name=fname))

    def find_header_text(self, fname, search_string):
        "identify the end of file header based on looking for a unique string"
        with open(fname, "r", encoding="utf8", errors="ignore") as f:
            pos = 0
            cur_line = f.readline()
            stripped = re.sub(r"\s", "", cur_line)
            while not stripped.startswith(search_string):
                if f.tell() == pos:
                    return False
                pos = f.tell()
                cur_line = f.readline()
                stripped = re.sub(r"\s", "", cur_line)

        f.close()
        if pos < os.path.getsize(fname):
            return True

        return False
