import pandas as pd
from psense_common import PSenseParser
from psense_common.psense_parser import is_float, SensorDataFormat
import unittest
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime, timedelta
import pytz


def is_dst():
    """Determine whether or not Daylight Savings Time (DST)
    is currently in effect"""

    x = datetime(
        datetime.now().year, 1, 1, 0, 0, 0, tzinfo=pytz.timezone("US/Eastern")
    )  # Jan 1 of this year
    y = datetime.now(pytz.timezone("US/Eastern"))

    # if DST is in effect, their offsets will be different
    return not (y.utcoffset() == x.utcoffset())


class TestPSenseParser(unittest.TestCase):
    def setUp(self):
        self.parser = PSenseParser(debugmode=True)
        pass

    def test_is_float(self):
        self.assertTrue(is_float(0))
        self.assertTrue(is_float("0"))
        self.assertTrue(is_float("0.5"))
        self.assertFalse(is_float("A"))
        self.assertFalse(is_float({"value": 0.5}))
        self.assertFalse(is_float([0.5]))

    def test_sensordataformat(self):
        obj = SensorDataFormat()

        # empty init
        self.assertIsNone(obj.name)
        self.assertEqual(obj.delimiter, ",")
        self.assertIsNone(obj.type_is_sensor)
        self.assertEqual(obj.has_timestamp, True)

        self.assertIsNone(obj.get_key("signal1"))
        self.assertIsNone(obj.get_header("signal1"))
        self.assertIsNone(obj.get_index("signal1"))
        self.assertEqual(obj.data_headers(), [])
        self.assertEqual(obj.data_keys(), [])
        self.assertEqual(obj.data_indices(), [])

        obj.set_key("signal1", ("test", 20))
        self.assertEqual(obj.get_key("signal1"), ("test", 20))
        self.assertEqual(obj.get_header("signal1"), "test")
        self.assertEqual(obj.get_index("signal1"), 20)

        self.assertEqual(obj.data_headers(), ["test"])
        self.assertEqual(obj.data_keys(), ["signal1"])
        self.assertEqual(obj.data_indices(), [20])

        obj = SensorDataFormat(
            name="test",
            delimiter="\t",
            has_timestamp=False,
            columns=dict(
                type=("TYPE", 1),
                timestamp=("timestamp", 0),
                signal1=("SIGNAL1", 2),
                vout1=("VOUT1", 4),
                enable1=("enable1", 3),
            ),
        )
        self.assertEqual(obj.name, "test")
        self.assertEqual(obj.delimiter, "\t")
        self.assertEqual(obj.has_timestamp, False)
        self.assertEqual(obj.get_key("signal1"), ("SIGNAL1", 2))
        self.assertIsNone(obj.get_key("doesntexist"))
        self.assertEqual(obj.get_header("signal1"), "SIGNAL1")
        self.assertEqual(obj.get_index("signal1"), 2)
        self.assertListEqual(
            obj.data_headers(), ["timestamp", "TYPE", "SIGNAL1", "enable1", "VOUT1"]
        )
        self.assertListEqual(
            obj.data_keys(), ["timestamp", "type", "signal1", "enable1", "vout1"]
        )
        self.assertListEqual(obj.data_indices(), [1, 0, 3, 4, 2])

    def test_force_source(self):
        self.assertRaises(IOError, self.parser.force_source, "not-a-real-data-type")
        type1 = "PSHIELD"
        self.parser.force_source(type1)
        self.assertEqual(self.parser.source, type1)
        type2 = "BWII-B02"
        self.parser.force_source(type2)
        self.assertEqual(self.parser.source, type2)

    def test_data_format(self):
        self.parser.force_source("BWII-S01-ECHEM")
        fmt = self.parser.data_format()
        self.assertEqual(fmt.type_is_sensor, "sensor_record")

        self.parser.force_source("BWII-S01-ZDATA")
        fmt = self.parser.data_format()
        self.assertEqual(fmt.type_is_sensor, "Z_sensor_record")

    def test_find_header_text(self):
        mock_type = "PSHIELD"
        search_string = self.parser.header_text[mock_type]

        m_open = MagicMock()
        m_methods = Mock()
        m_methods.tell.side_effect = [1, 2, 3, 4, 5, 15, 15]
        m_methods.readline.side_effect = [
            "random",
            "random",
            search_string,
            "random",
            "random",
            "random",
        ]
        m_open().__enter__.return_value = m_methods

        with patch("builtins.open", m_open, create=True):
            with patch("os.path.getsize", return_value=11):
                self.assertTrue(
                    self.parser.find_header_text("fake_file", search_string)
                )
                self.assertFalse(
                    self.parser.find_header_text(
                        "fake_file", "string-that-doesnt-exist"
                    )
                )

    def test_identify_file_source(self):

        self.assertRaises(
            FileNotFoundError, self.parser.identify_file_source, "fake_file"
        )

        self.parser.identify_file_source(fpath="tests/pshield_example")
        self.assertEqual(self.parser.source, "PSHIELD")
        self.parser.identify_file_source(fpath="tests/gamry_example")
        self.assertEqual(self.parser.source, "EXPLAIN")
        self.parser.identify_file_source("tests/__init__.py")
        self.assertEqual(self.parser.source, None)

    def test_read_variable_header_file(self):
        data, header = self.parser.read_variable_header_file(
            "tests/__init__.py", "NOT_FOUND_HEADER", sep=","
        )
        self.assertIsNone(data)
        self.assertIsNone(header)

        data, header = self.parser.read_variable_header_file(
            "tests/web1chan_example", "timestamp,Raw1,Vout1", sep=","
        )
        self.assertIsInstance(data, pd.DataFrame)
        self.assertListEqual(
            list(data.columns), ["timestamp", "Raw1", "Vout1", "Filt1"]
        )
        self.assertEqual(data.shape, (10, 4))
        self.assertEqual(len(header), 190)

    def test_parse_record(self):
        starting_time = datetime.now()

        self.parser.force_source("BWII-B04")
        data = ",".join(
            [
                starting_time.isoformat(),
                "sensor_record",
                "10",
                "1.1",
                "1000",
                "500",
                "1",
                "0",
                "2.1",
                "1010",
                "1",
                "0",
                "3.1",
                "1500",
                "1000",
                "0",
                "0",
                "3300",
            ]
        )
        res = self.parser.parse_record(data)
        self.assertTrue(
            datetime.fromisoformat(res[0]) - starting_time < timedelta(seconds=3)
        )
        self.assertEqual(res[1], [0.5, 0.51, 0.5])
        self.assertEqual(res[2], [1.1, 2.1, 3.1])
        self.assertEqual(res[3], [True, True, False])

        self.parser.force_source("BWII-B03")
        data = ",".join(
            [
                starting_time.isoformat(),
                "sensor_record",
                "10",
                "1.0",
                "1000",
                "500",
                "1",
                "0",
                "2.0",
                "1010",
                "1",
                "0",
                "3.0",
                "1500",
                "1",
                "0",
                "3300",
            ]
        )
        res = self.parser.parse_record(data)
        self.assertTrue(
            datetime.fromisoformat(res[0]) - starting_time < timedelta(seconds=3)
        )
        self.assertEqual(res[1], [0.5, 0.51, 1.0])
        self.assertEqual(res[2], [1.0, 2.0, 3.0])
        self.assertEqual(res[3], [True, True, True])

        data = data.replace("sensor_record", "incorrect_record_type")
        res = self.parser.parse_record(data)
        self.assertIsNone(res)

        data = ",".join(
            [
                starting_time.isoformat(),
                "sensor_record",
                "10",
                "1.0",
                "1000",
                "500",
                "0",
                "0",
                "2.0",
                "1010",
                "0",
                "0",
                "3.0",
                "1500",
                "0",
                "0",
                "3300",
            ]
        )
        res = self.parser.parse_record(data)
        self.assertEqual(res[3], [False, False, False])

        self.parser.force_source("BWII-B02")
        data = ",".join(
            [
                starting_time.isoformat(),  # timestamp
                "sensor_record",  # type
                "1",  # rnum
                "1",  # i
                ".2",  # vw
                ".1",  # vr
                "0",  # vc
                "1",  # on
                "0",  # disc
                "10",  # i
                ".4",  # vw
                ".2",  # vr
                ".1",  # vc
                "1",  # on
                "0",  # disc
                "0",  # batt
                "3260",  # vbatt
            ]
        )
        res = self.parser.parse_record(data)
        self.assertTrue(
            datetime.fromisoformat(res[0]) - starting_time < timedelta(seconds=3)
        )
        self.assertEqual(res[1], [0.0001, 0.0002])
        self.assertEqual(res[2], [1.0, 10.0])
        self.assertEqual(res[3], [True, True])
        data = ",".join(
            [
                starting_time.isoformat(),
                "sensor_record",  # type
                "1",  # rnum
                "1",  # i1
                ".2",  # vw
                ".1",  # vr
                "0",  # vc
                "0",  # on
                "0",  # disc
                "10",  # i
                ".4",  # w
                ".2",  # r
                ".1",  # c
                "0",  # on
                "0",  # disc
                "0",  # batt
                "3260",  # vbatt
            ]
        )
        res = self.parser.parse_record(data)
        self.assertEqual(res[3], [False, False])

        data = "1, 1554417874.000003, 12.51"
        self.parser.force_source("PSHIELD")
        res = self.parser.parse_record(data)
        self.assertEqual(res[0], "2019-04-04T15:44:34.000003")  # check local time (PDT)
        self.assertEqual(res[1], [None])
        self.assertEqual(res[2], [12.51])
        self.assertEqual(res[3], [True])

        data = "1, 1615435200, 12.51"
        res = self.parser.parse_record(data)
        self.assertEqual(res[0], "2021-03-10T20:00:00")  # check local time (PST)

        data = "0.399550	7.3E-9"
        self.parser.force_source("VFP")
        res = self.parser.parse_record(data)
        self.assertTrue(
            datetime.fromisoformat(res[0]) - starting_time < timedelta(seconds=3)
        )
        self.assertEqual(res[1], [0.39955])
        self.assertEqual(res[2], [7.3])
        self.assertEqual(res[3], [True])

        data = "2015-12-26 20:19:18,0.72,0.3,0.72"
        self.parser.force_source("WEB-APP")
        res = self.parser.parse_record(data)
        self.assertEqual(res[0], "2015-12-26T20:19:18")
        self.assertEqual(res[1], [0.3])
        self.assertEqual(res[2], [0.72])
        self.assertTrue(res[3])

        data = "2020-02-10 10:59:24,0.83,0.507,-7.89,-0.456,5.05,0.123,0.83,1.3,0.03"
        self.parser.force_source("WEB-APP")
        res = self.parser.parse_record(data)
        self.assertEqual(res[0], "2020-02-10T10:59:24")
        self.assertEqual(res[1], [0.507, -0.456, 0.123])
        self.assertEqual(res[2], [0.83, -7.89, 5.05])
        self.assertEqual(res[3], [True] * 3)

        res = self.parser.parse_record(data, num_channels=2)
        self.assertEqual(res[0], "2020-02-10T10:59:24")
        self.assertEqual(res[1], [0.507, -0.456])
        self.assertEqual(res[2], [0.83, -7.89])
        self.assertEqual(res[3], [True] * 2)

        data = "1.000e+1, 4.020e-8, 5.779e-8, 6.402e-8, 7.063e-8"
        self.parser.force_source("CHI")
        res = self.parser.parse_record(data)
        self.assertEqual(res[1], [None] * 4)
        self.assertEqual(res[2], [4.02e-8, 5.779e-8, 6.402e-8, 7.063e-8])
        self.assertEqual(res[3], [True] * 4)
        data = "1.000e+1, 1e-8, 2e-8, 3e-8, 4e-8, -1e-8, -2e-8, -3e-8, -4e-8"
        res = self.parser.parse_record(data)
        self.assertEqual(res[1], [None] * 8)
        self.assertEqual(res[2], [1e-8, 2e-8, 3e-8, 4e-8, -1e-8, -2e-8, -3e-8, -4e-8])
        self.assertEqual(res[3], [True] * 8)

    def test_load_no_source(self):
        testfile = "tests/pshield_example"

        # fake source
        self.parser.source = "fake-source"
        self.assertRaises(ValueError, self.parser.load_rawfile, testfile, None, None)

    def test_load_pshield(self):
        testfile = "tests/pshield_example"
        # pshield file
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[-1], 0.5)
        self.assertEqual(df["signal1"].iloc[-1], 5.29)
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2018-07-23 17:28:08.22").round(freq="s"),
        )

    def test_load_rawcsv(self):
        testfile = "tests/rawcsv_data_example"
        self.parser.force_source("RAWCSV")

        self.assertEqual(self.parser.source, "RAWCSV")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[0], 0.5)
        self.assertEqual(df["signal1"].iloc[0], -1)
        self.assertTrue(df["enable1"].iloc[0])
        self.assertEqual(df["vout2"].iloc[0], -0.5)
        self.assertEqual(df["signal2"].iloc[0], 0)
        self.assertFalse(df["enable2"].iloc[0])
        self.assertEqual(df["vout3"].iloc[0], -0.5)
        self.assertEqual(df["signal3"].iloc[0], 0)
        self.assertFalse(df["enable3"].iloc[0])

        self.assertEqual(df["vout1"].iloc[-1], 0.7)
        self.assertEqual(df["signal1"].iloc[-1], -9)
        self.assertTrue(df["enable1"].iloc[-1])
        self.assertEqual(df["vout2"].iloc[-1], -0.9)
        self.assertEqual(df["signal2"].iloc[-1], 0.1)
        self.assertTrue(df["enable2"].iloc[-1])
        self.assertEqual(df["vout3"].iloc[-1], 0.9)
        self.assertEqual(df["signal3"].iloc[-1], -0.1)
        self.assertTrue(df["enable3"].iloc[-1])
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2022-01-15 17:27:06"),
        )

    def test_load_bwii_b02_download(self):
        testfile = "tests/bwii_b02_download_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "BWII-B02")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[-1], 0.487)
        self.assertEqual(df["signal1"].iloc[-1], 1.76)
        self.assertEqual(df["vout2"].iloc[-1], 0)
        self.assertEqual(df["signal2"].iloc[-1], 0)
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2019-03-04 16:37:42"),
        )

        start_time = "2019/01/01 12:00"
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[-1], 0.487)
        self.assertEqual(df["signal1"].iloc[-1], 1.76)
        self.assertEqual(df["vout2"].iloc[-1], 0)
        self.assertEqual(df["signal2"].iloc[-1], 0)
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2019-01-01 12:13:43"),
        )

        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[-1], 0.487)
        self.assertEqual(df["signal1"].iloc[-1], 1.76)
        self.assertEqual(df["vout2"].iloc[-1], 0)
        self.assertEqual(df["signal2"].iloc[-1], 0)
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2019-01-01 12:00:00"),
        )

    def test_load_bwii_b03_download(self):
        testfile = "tests/bwii_b03_download_example"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[1], 0.501)
        self.assertEqual(df["signal1"].iloc[1], 0.175)
        self.assertEqual(df["vout2"].iloc[1], 0.502)
        self.assertEqual(df["signal2"].iloc[1], 1.75)
        self.assertEqual(df["vout3"].iloc[1], 1)
        self.assertEqual(df["signal3"].iloc[1], 17.5)

        self.assertEqual(df["vout1"].iloc[-1], 0.501)
        self.assertEqual(df["signal1"].iloc[-1], 175)
        self.assertEqual(df["vout2"].iloc[-1], -0.488)
        self.assertEqual(df["signal2"].iloc[-1], 0)
        self.assertEqual(df["vout3"].iloc[-1], -0.488)
        self.assertEqual(df["signal3"].iloc[-1], 0)
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2020-01-01 19:32:17"),
        )

        self.assertTrue(df["enable1"].iloc[0])
        self.assertFalse(df["enable2"].iloc[0])
        self.assertFalse(df["enable3"].iloc[0])
        self.assertFalse(df["enable3"].iloc[-1])

        start_time = "2019/01/01 12:00"
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(
            df["timestamp"].iloc[0].round(freq="s"), pd.Timestamp("2019-01-01 12:00:00")
        )
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2019-01-01 12:02:19"),
        )

        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertEqual(
            df["timestamp"].iloc[0].round(freq="s"), pd.Timestamp("2019-01-01 11:57:41")
        )
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2019-01-01 12:00:00"),
        )

    def test_load_bwii_b03_realtime(self):
        # files downloaded from BWII_Util.exe have extra whitespace. Make sure they are loaded properly
        testfile = "tests/bwii_b03_realtime_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "BWII-B03")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(len(df.index), 20)
        self.assertEqual(df["signal1"].iloc[0], 41.5901)
        self.assertEqual(df["signal2"].iloc[0], 0.0520)
        self.assertEqual(df["signal3"].iloc[0], 0.0500)
        self.assertEqual(df["signal1"].iloc[-1], 9.5240)
        self.assertEqual(df["signal2"].iloc[-1], 0.0510)
        self.assertEqual(df["signal3"].iloc[-1], -34.5678)

        self.assertEqual(df["vout1"].iloc[0], 0.505)
        self.assertEqual(df["vout2"].iloc[0], 0.501)
        self.assertEqual(df["vout3"].iloc[0], 0.500)
        self.assertEqual(df["vout1"].iloc[-1], 0.505)
        self.assertEqual(df["vout2"].iloc[-1], -0.500)
        self.assertEqual(df["vout3"].iloc[-1], 0.499)

        self.assertTrue(df["enable1"].iloc[0])
        self.assertTrue(df["enable2"].iloc[0])
        self.assertTrue(df["enable3"].iloc[0])
        self.assertTrue(df["enable1"].iloc[-1])
        self.assertFalse(df["enable2"].iloc[-1])
        self.assertFalse(df["enable3"].iloc[-1])

    def test_load_bwii_b03_corruptfile(self):
        # if 2 downloads are merged, make sure the headers are cleaned up and rows are preserved
        testfile = "tests/bwii_b03_merged_download_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "BWII-B03")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(len(df.index), 8)
        self.assertEqual(df["signal1"].iloc[0], 30)
        self.assertEqual(df["signal2"].iloc[0], 17)
        self.assertEqual(df["signal3"].iloc[0], 0)
        self.assertEqual(df["signal1"].iloc[-1], 4)
        self.assertEqual(df["signal2"].iloc[-1], 3)
        self.assertEqual(df["signal3"].iloc[-1], 0)

        self.assertEqual(df["vout1"].iloc[0], 0.504)
        self.assertEqual(df["vout2"].iloc[0], 0.503)
        self.assertEqual(df["vout3"].iloc[0], -0.989)
        self.assertEqual(df["vout1"].iloc[-1], 0.605)
        self.assertEqual(df["vout2"].iloc[-1], 0.604)
        self.assertEqual(df["vout3"].iloc[-1], -0.989)

        self.assertTrue(df["enable1"].iloc[0])
        self.assertTrue(df["enable2"].iloc[0])
        self.assertFalse(df["enable3"].iloc[0])
        self.assertTrue(df["enable1"].iloc[-1])
        self.assertTrue(df["enable2"].iloc[-1])
        self.assertFalse(df["enable3"].iloc[-1])

    def test_load_bwii_b03_drop_duplicates(self):
        # if 2 downloads are merged, make sure the headers are cleaned up and rows are preserved
        testfile = "tests/bwii_b03_duplicates_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "BWII-B03")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(len(df.index), 2)
        self.assertEqual(df["signal1"].iloc[0], 30)
        self.assertEqual(df["signal1"].iloc[-1], 26)
        self.assertEqual(df["signal2"].iloc[0], 17)
        self.assertEqual(df["signal2"].iloc[-1], 15)

    def test_load_bwii_b04_download(self):
        # check file format from b04 device (mini-iso)
        testfile = "tests/bwii_b04_download_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "BWII-B04")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[1], 0.603)
        self.assertEqual(df["signal1"].iloc[1], 60)
        self.assertEqual(df["vout2"].iloc[1], 0.600)
        self.assertEqual(df["signal2"].iloc[1], 50)
        self.assertEqual(df["vout3"].iloc[1], -0.500)
        self.assertEqual(df["signal3"].iloc[1], -10)

        self.assertEqual(df["vout1"].iloc[-1], 0.200)
        self.assertEqual(df["signal1"].iloc[-1], 11)
        self.assertEqual(df["vout2"].iloc[-1], 0.100)
        self.assertEqual(df["signal2"].iloc[-1], 12)
        self.assertEqual(df["vout3"].iloc[-1], -0.100)
        self.assertEqual(df["signal3"].iloc[-1], -13)
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2022-01-10 00:15:00"),
        )

        self.assertTrue(df["enable1"].iloc[0])
        self.assertFalse(df["enable2"].iloc[0])
        self.assertFalse(df["enable3"].iloc[0])
        self.assertFalse(df["enable1"].iloc[-1])
        self.assertTrue(df["enable2"].iloc[-1])
        self.assertFalse(df["enable3"].iloc[-1])

    def test_load_bwii_s01_download(self):
        # only does echem data right now
        testfile = "tests/bwii_s01_download_echem_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "BWII-S01-ECHEM")

        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data

        self.assertEqual(df.shape[0], 4)
        self.assertEqual(df["signal1"].tolist(), [25, 25, 50, 50])
        self.assertEqual(df["signal2"].tolist(), [50, 25, 50, 25])
        self.assertEqual(df["vout1"].tolist(), [0.5] * 4)
        self.assertEqual(df["vout2"].tolist(), [0.3, 0.301, 0.302, 0.303])
        self.assertEqual(df["enable1"].tolist(), [True, True, False, False])
        self.assertEqual(df["discard2"].tolist(), [False, False, True, True])
        self.assertEqual(
            df["timestamp"].tolist(),
            [
                pd.Timestamp("2021-03-22 22:28:30"),
                pd.Timestamp("2021-03-22 22:29:00"),
                pd.Timestamp("2021-03-22 22:29:30"),
                pd.Timestamp("2021-03-22 22:30:00"),
            ],
        )

        start_time = "2021/01/01 12:00"
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(
            df["timestamp"].tolist(),
            [
                pd.Timestamp("2021-01-01 12:00:00"),
                pd.Timestamp("2021-01-01 12:00:30"),
                pd.Timestamp("2021-01-01 12:01:00"),
                pd.Timestamp("2021-01-01 12:01:30"),
            ],
        )

        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertEqual(
            df["timestamp"].to_list(),
            [
                pd.Timestamp("2021-01-01 11:58:30"),
                pd.Timestamp("2021-01-01 11:59:00"),
                pd.Timestamp("2021-01-01 11:59:30"),
                pd.Timestamp("2021-01-01 12:00:00"),
            ],
        )

    def test_load_bwii_s01_realtime(self):
        # files downloaded from BWII_Util.exe have extra whitespace. Make sure they are loaded properly
        testfile = "tests/bwii_s01_realtime_echem_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "BWII-S01-ECHEM")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df.shape[0], 4)
        self.assertEqual(df["signal1"].tolist(), [25, 25, 50, 50])
        self.assertEqual(df["signal2"].tolist(), [50, 25, 50, 25])
        self.assertEqual(df["vout1"].tolist(), [0.5] * 4)
        self.assertEqual(df["vout2"].tolist(), [0.3, 0.301, 0.302, 0.303])
        self.assertEqual(df["enable1"].tolist(), [False, True, False, True])
        self.assertEqual(df["discard2"].tolist(), [True, False, True, False])

    def test_load_bwii_stream(self):
        # b02 data
        testfile = "tests/bwii_b02_stream_example"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df["vout1"].iloc[-1], 0)
        self.assertEqual(df["signal1"].iloc[-1], 1)
        self.assertEqual(df["vout2"].iloc[-1], 2)
        self.assertEqual(df["signal2"].iloc[-1], 3)
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2019-03-04T13:08:54"),
        )

        self.assertTrue(df["enable1"].iloc[-1])
        self.assertTrue(df["enable2"].iloc[0])

        # b03 data
        testfile = "tests/bwii_b03_stream_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "BWII-STREAM")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(len(df.index), 10)
        self.assertEqual(df["signal1"].iloc[0], 0.15)
        self.assertEqual(df["signal2"].iloc[0], 11.698)
        self.assertEqual(df["signal3"].iloc[0], 0)
        self.assertEqual(df["vout1"].iloc[0], 0.504)
        self.assertEqual(df["vout2"].iloc[0], 0.501)
        self.assertEqual(df["vout3"].iloc[0], 0)

        self.assertEqual(df["signal1"].iloc[-1], 0.127)
        self.assertEqual(df["signal2"].iloc[-1], 10.5)
        self.assertEqual(df["signal3"].iloc[-1], 0)
        self.assertEqual(df["vout1"].iloc[-1], 0.505)
        self.assertEqual(df["vout2"].iloc[-1], 0.502)
        self.assertEqual(df["vout3"].iloc[-1], 0)

        self.assertTrue(df["enable1"].iloc[0])
        self.assertTrue(df["enable2"].iloc[0])
        self.assertTrue(df["enable3"].iloc[0])
        self.assertTrue(df["enable1"].iloc[-1])
        self.assertTrue(df["enable2"].iloc[-1])
        self.assertTrue(df["enable3"].iloc[-1])

    def test_load_dev_controller_download(self):
        testfile = "tests/dev_controller_download_b03_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "DEV-B03-AGGREG")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(len(df.index), 3)
        self.assertEqual(df["signal1"].iloc[0], -1)
        self.assertEqual(df["signal2"].iloc[0], -10)
        self.assertEqual(df["signal1"].iloc[-1], 10)
        self.assertEqual(df["signal2"].iloc[-1], 20)

        self.assertTrue(df["discard1"].iloc[0])
        self.assertTrue(df["discard2"].iloc[0])
        self.assertFalse(df["discard3"].iloc[0])
        self.assertFalse(df["discard1"].iloc[-1])
        self.assertFalse(df["discard2"].iloc[-1])
        self.assertFalse(df["discard3"].iloc[-1])

        self.assertTrue(df["enable1"].iloc[0])
        self.assertTrue(df["enable2"].iloc[0])
        self.assertFalse(df["enable3"].iloc[0])
        self.assertFalse(df["enable1"].iloc[-1])
        self.assertTrue(df["enable2"].iloc[-1])
        self.assertFalse(df["enable3"].iloc[-1])

        testfile = "tests/dev_controller_download_s01_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "DEV-S01-AGGREG")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(len(df.index), 2)
        self.assertFalse("enable3" in df.columns)
        self.assertEqual(
            df["timestamp"].iloc[0],
            pd.Timestamp("2021-01-01T08:00:00"),
        )
        self.assertEqual(
            df["timestamp"].iloc[-1],
            pd.Timestamp("2021-01-10T09:08:07"),
        )

        self.assertEqual(df["signal1"].iloc[0], 20)
        self.assertEqual(df["signal2"].iloc[0], 15)
        self.assertEqual(df["signal1"].iloc[-1], 15)
        self.assertEqual(df["signal2"].iloc[-1], 10)

        self.assertEqual(df["vout1"].iloc[0], 0.400)
        self.assertEqual(df["vout2"].iloc[0], 0.600)
        self.assertEqual(df["vout1"].iloc[-1], 0.404)
        self.assertEqual(df["vout2"].iloc[-1], 0.700)

        self.assertFalse(df["discard1"].iloc[0])
        self.assertTrue(df["discard2"].iloc[0])
        self.assertTrue(df["discard1"].iloc[-1])
        self.assertFalse(df["discard2"].iloc[-1])

        self.assertFalse(df["enable1"].iloc[0])
        self.assertFalse(df["enable2"].iloc[0])
        self.assertTrue(df["enable1"].iloc[-1])
        self.assertTrue(df["enable2"].iloc[-1])

        testfile = "tests/dev_controller_download_b04_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "DEV-B04-AGGREG")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(len(df.index), 10)
        self.assertEqual(
            df["timestamp"].iloc[0],
            pd.Timestamp("2022-06-04 17:46:16"),
        )
        self.assertEqual(
            df["timestamp"].iloc[-1],
            pd.Timestamp("2022-06-04 17:50:46"),
        )
        self.assertListEqual(
            df["signal1"].tolist(),
            [14.0, 15.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 17.0],
        )
        self.assertListEqual(
            df["signal2"].tolist(),
            [90.0, 93.0, 97.0, 97.0, 93.0, 88.0, 84.0, 79.0, 76.0, 72.0],
        )
        self.assertListEqual(
            df["signal3"].tolist(),
            [-1.6, -1.5, -1.5, -1.5, -1.4, -1.4, -1.3, -1.3, -1.2, -1.5],
        )
        self.assertListEqual(
            df["vout1"].tolist(),
            [0.753, 0.754, 0.755, 0.754, 0.753, 0.754, 0.753, 0.753, 0.753, 0.754],
        )
        self.assertListEqual(
            df["vout2"].tolist(),
            [0.753, 0.753, 0.754, 0.754, 0.753, 0.753, 0.754, 0.753, 0.753, 0.754],
        )
        self.assertListEqual(df["vout3"].tolist(), 10 * [0.75])

        self.assertFalse(df["discard1"].iloc[0])
        self.assertFalse(df["discard2"].iloc[0])
        self.assertFalse(df["discard3"].iloc[0])
        self.assertFalse(df["discard1"].iloc[-1])
        self.assertTrue(df["discard2"].iloc[-1])
        self.assertTrue(df["discard3"].iloc[-1])

        self.assertFalse(df["enable1"].iloc[0])
        self.assertTrue(df["enable2"].iloc[0])
        self.assertFalse(df["enable3"].iloc[0])

        self.assertTrue(df["enable1"].iloc[-1])
        self.assertFalse(df["enable2"].iloc[-1])
        self.assertTrue(df["enable3"].iloc[-1])

    def test_load_dev_controller_stream(self):
        testfile = "tests/dev_controller_stream_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "DEV-STREAM")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(len(df.index), 10)
        self.assertEqual(df["signal1"].iloc[0], 0.15)
        self.assertEqual(df["signal2"].iloc[0], 11.698)
        self.assertEqual(df["signal3"].iloc[0], 0)
        self.assertEqual(df["vout1"].iloc[0], 0.504)
        self.assertEqual(df["vout2"].iloc[0], 0.501)
        self.assertEqual(df["vout3"].iloc[0], 0)

        self.assertEqual(df["signal1"].iloc[-1], 0.127)
        self.assertEqual(df["signal2"].iloc[-1], 10.5)
        self.assertEqual(df["signal3"].iloc[-1], 0)
        self.assertEqual(df["vout1"].iloc[-1], 0.505)
        self.assertEqual(df["vout2"].iloc[-1], 0.502)
        self.assertEqual(df["vout3"].iloc[-1], 99)

        self.assertTrue(df["enable1"].iloc[0])
        self.assertFalse(df["enable2"].iloc[0])
        self.assertTrue(df["enable3"].iloc[0])
        self.assertTrue(df["enable1"].iloc[-1])
        self.assertTrue(df["enable2"].iloc[-1])
        self.assertFalse(df["enable3"].iloc[-1])

        testfile = "tests/dev_controller_stream_duplicate_header_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "DEV-STREAM")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))

        df = self.parser.data
        self.assertEqual(len(df.index), 6)
        self.assertEqual(df["signal1"].iloc[2], 0.123)
        self.assertEqual(df["signal2"].iloc[2], 0.456)
        self.assertEqual(df["signal3"].iloc[2], 0.789)
        self.assertEqual(df["signal1"].iloc[-1], 0.789)
        self.assertEqual(df["signal2"].iloc[-1], 0.123)
        self.assertEqual(df["signal3"].iloc[-1], 0.456)

        self.assertEqual(df["timestamp"].iloc[2], pd.Timestamp("2020-12-15T17:22:07"))
        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2020-12-15T18:22:07"))

    def test_load_webapp_v1v2(self):
        # web app file
        testfile = "tests/web1chan_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "WEB-APP")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(len(df.columns), 4)

        self.assertEqual(df["vout1"].iloc[-1], 0.3)
        self.assertEqual(df["signal1"].iloc[-1], 2.77)
        self.assertTrue(df["enable1"].iloc[-1])

        self.assertEqual(df["timestamp"].iloc[-1], pd.Timestamp("2019-07-26 17:12:30"))

        testfile = "tests/web2chan_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "WEB-APP")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(len(df.columns), 7)

        self.assertEqual(df["vout1"].iloc[-1], 0.5)
        self.assertEqual(df["signal1"].iloc[-1], 5)
        self.assertTrue(df["enable1"].iloc[-1])

        self.assertEqual(df["vout2"].iloc[-1], 0.4)
        self.assertEqual(df["signal2"].iloc[-1], 15)
        self.assertTrue(df["enable2"].iloc[-1])

        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2019-07-09 17:35:24"),
        )

        testfile = "tests/web3chan_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "WEB-APP")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(len(df.columns), 10)

        self.assertEqual(df["vout1"].iloc[-1], 0.508)
        self.assertEqual(df["signal1"].iloc[-1], 2.48)
        self.assertTrue(df["enable1"].iloc[-1])

        self.assertEqual(df["vout2"].iloc[-1], -0.501)
        self.assertEqual(df["signal2"].iloc[-1], 0.03)
        self.assertTrue(df["enable2"].iloc[-1])

        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2020-02-10 11:04:54"),
        )

    def test_load_vfp600(self):
        # vfp600
        start_time = "2019/01/01 12:00"
        testfile = "tests/vfp_example"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(
            df["timestamp"].iloc[0].round(freq="s"),
            pd.Timestamp(start_time).round(freq="s"),
        )
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertTrue(df["timestamp"].iloc[0] < pd.Timestamp(start_time))
        ts = [df["timestamp"].iloc[-1], pd.Timestamp(start_time)]
        self.assertTrue(pd.Timedelta(max(ts) - min(ts)).seconds < 1)

        self.assertEqual(df["vout1"].iloc[-1], 0.39955)
        self.assertEqual(round(df["signal1"].iloc[-1], 2), 3.8)
        self.assertTrue(df["enable1"].iloc[-1])

        # vfp600 #2
        start_time = "2019/01/01 12:00"
        testfile = "tests/vfp_example2"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(
            df["timestamp"].iloc[0].round(freq="s"),
            pd.Timestamp(start_time).round(freq="s"),
        )
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertTrue(df["timestamp"].iloc[0] < pd.Timestamp(start_time))
        ts = [df["timestamp"].iloc[-1], pd.Timestamp(start_time)]
        self.assertTrue(pd.Timedelta(max(ts) - min(ts)).seconds < 1)

        self.assertEqual(df["vout1"].iloc[-2], 0.101215)
        self.assertEqual(round(df["signal1"].iloc[-2], 2), 0.19)
        self.assertEqual(df["vout1"].iloc[-1], 0.101219)
        self.assertEqual(round(df["signal1"].iloc[-1], 3), 0.244)
        self.assertTrue(df["enable1"].iloc[-1])

    def test_load_explain(self):
        # gamry explain
        start_time = "2018/09/11 12:00"
        testfile = "tests/gamry_example"
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(
            df["timestamp"].iloc[0].round(freq="s"),
            pd.Timestamp(start_time).round(freq="s"),
        )
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertEqual(
            df["timestamp"].iloc[0].round(freq="s"),
            pd.Timestamp(start_time).round(freq="s"),
        )

        self.assertEqual(round(1000 * df["vout1"].iloc[-1]) / 1000, 0.500)
        self.assertEqual(round(1000 * df["signal1"].iloc[-1]) / 1000, 3.605)
        self.assertTrue(df["enable1"].iloc[-1])

    def test_load_chinstruments(self):
        testfile = "tests/chinstruments_example"
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, "CHI")
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data

        self.assertEqual(
            df["timestamp"].iloc[0].round(freq="s"), pd.Timestamp("2020/07/15 15:27:12")
        )
        self.assertEqual(
            df["timestamp"].iloc[-1].round(freq="s"),
            pd.Timestamp("2020/07/15 15:37:12"),
        )

        self.assertEqual(df["vout1"].iloc[0], 0.5)
        self.assertEqual(df["vout1"].iloc[-1], 0.5)
        self.assertEqual(df["vout2"].iloc[0], -0.5)
        self.assertEqual(df["vout2"].iloc[-1], -0.5)
        self.assertEqual(df["vout3"].iloc[0], -0.3)
        self.assertEqual(df["vout3"].iloc[-1], -0.3)
        self.assertEqual(df["vout4"].iloc[0], 1.0)
        self.assertEqual(df["vout4"].iloc[-1], 1.0)

        self.assertTrue(df["enable1"].iloc[-1])
        self.assertTrue(df["enable1"].iloc[0])
        self.assertTrue(df["enable2"].iloc[-1])
        self.assertTrue(df["enable2"].iloc[0])
        self.assertTrue(df["enable3"].iloc[-1])
        self.assertTrue(df["enable3"].iloc[0])
        self.assertTrue(df["enable4"].iloc[-1])
        self.assertTrue(df["enable4"].iloc[0])

        self.assertEqual(df["signal1"].iloc[-1], 0.3608)
        self.assertEqual(df["signal2"].iloc[-1], 20.09)
        self.assertEqual(df["signal3"].iloc[-1], 8)
        self.assertEqual(df["signal4"].iloc[-1], 39.8)
