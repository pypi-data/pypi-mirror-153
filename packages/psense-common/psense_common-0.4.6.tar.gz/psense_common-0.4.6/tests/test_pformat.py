import unittest
from unittest.mock import patch
from psense_common import psense_format
from datetime import datetime


class TestPFormat(unittest.TestCase):
    def setUp(self):
        self.format = psense_format.psense_exp_title()

    def test_invalid_input(self):
        self.assertEqual(self.format.decode(""), {"study": [], "sensor": []})

    def test_valid_input_legacy(self):
        code1 = "19C12B904B02-1111-222-33-O02CPBX"
        self.assertEqual(
            self.format.decode(code1),
            {
                "study": {
                    "start": "2019-03-12",
                    "type": "Beaker",
                    "run": "04",
                    "device": "B02",
                },
                "sensor": {
                    "code": "1111-222-33",
                    "count": "O",
                    "vsn": "02",
                    "electrodes": [
                        {
                            "type": "Oxygen",
                            "electrode": "Circular",
                            "stack": "Planar",
                            "process": "Blanket",
                            "extras": "X",
                        }
                    ],
                },
            },
        )

        code2 = "19C11A001B04-0205-205-LA-G11CPVX"
        self.assertEqual(
            self.format.decode(code2),
            {
                "study": {
                    "start": "2019-03-11",
                    "type": "Heat Block",
                    "run": "01",
                    "device": "B04",
                },
                "sensor": {
                    "code": "0205-205-LA",
                    "count": "G",
                    "vsn": "11",
                    "electrodes": [
                        {
                            "type": "Glucose",
                            "electrode": "Circular",
                            "stack": "Planar",
                            "process": "Volcano",
                            "extras": "X",
                        }
                    ],
                },
            },
        )

        code3 = "19H01P101B08-500A-123-LA-X13RPSN"
        self.assertEqual(
            self.format.decode(code3),
            {
                "study": {
                    "start": "2019-08-01",
                    "type": "Prototype",
                    "run": "01",
                    "device": "B08",
                },
                "sensor": {
                    "code": "500A-123-LA",
                    "count": "X",
                    "vsn": "13",
                    "electrodes": [
                        {
                            "type": "Multi (legacy)",
                            "electrode": "Rectangular",
                            "stack": "Planar",
                            "process": "Standard",
                            "extras": "NAD+",
                        }
                    ],
                },
            },
        )

    def test_valid_input_multianalyte(self):
        code1 = "19C12B904B02-1111-222-33-199OCB"
        # new format, but just 1 electrode
        self.assertEqual(
            self.format.decode(code1),
            {
                "study": {
                    "start": "2019-03-12",
                    "type": "Beaker",
                    "run": "04",
                    "device": "B02",
                },
                "sensor": {
                    "code": "1111-222-33",
                    "count": "1",
                    "vsn": "99",
                    "electrodes": [
                        {
                            "type": "Oxygen",
                            "electrode": "Circular",
                            "process": "Blanket",
                        }
                    ],
                },
            },
        )

        # dual analyte
        code2 = "20G11AN07B04-0205-205-LA-215GCVOCS"
        self.assertEqual(
            self.format.decode(code2),
            {
                "study": {
                    "start": "2020-07-11",
                    "type": "Pre-Clinical",
                    "run": "07",
                    "device": "B04",
                },
                "sensor": {
                    "code": "0205-205-LA",
                    "count": "2",
                    "vsn": "15",
                    "electrodes": [
                        {
                            "type": "Glucose",
                            "electrode": "Circular",
                            "process": "Volcano",
                        },
                        {
                            "type": "Oxygen",
                            "electrode": "Circular",
                            "process": "Standard",
                        },
                    ],
                },
            },
        )

    def test_partial_input(self):
        code_study_only = "19A01A001B04"
        self.assertEqual(
            self.format.decode(code_study_only),
            {
                "study": {
                    "start": "2019-01-01",
                    "type": "Heat Block",
                    "run": "01",
                    "device": "B04",
                },
                "sensor": [],
            },
        )

        code_partial = "19C11JJXXM99-WE-RE-X-X99CXXX"
        self.assertEqual(
            self.format.decode(code_partial),
            {
                "study": {
                    "start": "2019-03-11",
                    "type": None,
                    "run": "XX",
                    "device": "M99",
                },
                "sensor": {
                    "code": "WE-RE-X",
                    "count": "X",
                    "vsn": "99",
                    "electrodes": [
                        {
                            "type": "Multi (legacy)",
                            "electrode": "Circular",
                            "stack": "Other",
                            "process": None,
                            "extras": "X",
                        }
                    ],
                },
            },
        )

    def test_yn_input(self):
        with patch("builtins.input", return_value=""):
            self.assertTrue(psense_format.yn_input("message"))
            self.assertFalse(psense_format.yn_input("message", "n"))

        with patch("builtins.input", return_value="y"):
            self.assertTrue(psense_format.yn_input("message"))
            self.assertTrue(psense_format.yn_input("message", "n"))

    def test_answer_input(self):
        with patch("builtins.input", return_value=""):
            self.assertEqual(
                psense_format.answer_input(
                    "message", "[0-9]", default="0", is_required=False
                ),
                "0",
            )

        with patch("builtins.input", return_value="1"):
            self.assertEqual(
                psense_format.answer_input(
                    "message", "[0-9]", default="0", is_required=False
                ),
                "1",
            )
            self.assertEqual(
                psense_format.answer_input(
                    "message", ["0", "1", "2"], default="0", is_required=False
                ),
                "1",
            )

    def test_timestamp_input(self):
        with patch("builtins.input", return_value="2021-01-01 12:30"):
            self.assertEqual(
                psense_format.timestamp_input("message"),
                datetime(2021, 1, 1, 12, 30, 0),
            )

        with patch(
            "builtins.input",
            side_effect=[
                "",
                "0",
                "2021/01/02 12:30",
                "2021-01-03 12:30:30",
                "2021-01-04 12:30",
            ],
        ):
            self.assertEqual(
                psense_format.timestamp_input("message"),
                datetime(2021, 1, 4, 12, 30, 0),
            )

        with patch(
            "builtins.input", side_effect=["2021-01-02 12:30", "2021-01-03 12:30:30"]
        ):
            self.assertEqual(
                psense_format.timestamp_input("message", use_seconds=True),
                datetime(2021, 1, 3, 12, 30, 30),
            )

    def test_exptype_input(self):
        with patch("builtins.input", return_value=""):
            self.assertTrue(psense_format.exptype_input())

        with patch("builtins.input", return_value="1"):
            self.assertTrue(psense_format.exptype_input())

        with patch("builtins.input", return_value="2"):
            self.assertFalse(psense_format.exptype_input())

    def test_setup_experiment(self):
        self.assertRaises(AssertionError, psense_format.setup_new_experiment, 0)

        datecode = "{}{}{}".format(
            datetime.now().strftime("%y"),
            chr(int(datetime.now().strftime("%m")) + 64),
            datetime.now().strftime("%d"),
        )

        with patch(
            "builtins.input",
            side_effect=["A1", "", "9999", "", "", "99", "1", "K", "", "S"],
        ):
            res = psense_format.setup_new_experiment("B01")
            self.assertEqual(res[5:], "A101B01-9999-000-00-199KCS")
            self.assertEqual(res[:5], datecode)

        with patch(
            "builtins.input",
            side_effect=[
                "AN",
                "5",
                "9999",
                "",
                "",
                "99",
                "3",
                "G",
                "C",
                "V",
                "L",
                "R",
                "V",
                "A",
                "",
                "W",
            ],
        ):
            res = psense_format.setup_new_experiment("B21")
            self.assertEqual(res[5:], "AN05B21-9999-000-00-399GCVLRVACW")
            self.assertEqual(res[:5], datecode)

        with patch(
            "builtins.input",
            side_effect=[
                "M1",
                "B1",
                "A",
                "99",
                "8888",
                "777",
                "66",
                "L",
                "88",
                "L",
                "1",
                "L",
                "AAA",
                "",
                "",
                "B",
            ],
        ):
            res = psense_format.setup_new_experiment("F01")
            self.assertEqual(res[5:], "B199F01-8888-777-66-188LCB")


if __name__ == "__main__":
    unittest.main()
