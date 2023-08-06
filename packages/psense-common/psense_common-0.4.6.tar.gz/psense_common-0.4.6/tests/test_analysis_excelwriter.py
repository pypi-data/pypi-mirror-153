import unittest
import pandas as pd
import xlsxwriter
import os
from psense_common import PSenseParser
from psense_common.analysis import ExcelWriter, PSenseCalibration
import datetime


def initialize_workbook(workbook_file):
    return ExcelWriter(workbook_file)


def cleanup_workbook(workbook_file):
    if os.path.isfile(workbook_file):
        os.remove(workbook_file)


def convert_excelepoch_to_timestamp(excel_date):
    epoch = datetime.datetime(1899, 12, 30)
    days = int(excel_date)
    fraction = excel_date - days

    # Get the the integer and decimal seconds in Excel's millisecond resolution.
    seconds = int(round(fraction * 86400000.0))
    seconds, milliseconds = divmod(seconds, 1000)

    return pd.Timestamp(epoch + datetime.timedelta(days, seconds, 0, milliseconds))


class TestExcelWriter(unittest.TestCase):
    def setUp(self):
        self.workbook_path = os.path.join(os.path.curdir, "test.xlsx")

    def test_init(self):
        xlsx = initialize_workbook(self.workbook_path)
        self.assertIsNotNone(xlsx.writer)
        self.assertIsNotNone(xlsx.workbook)
        xlsx.writer.close()
        self.assertTrue(os.path.isfile(self.workbook_path))
        cleanup_workbook(self.workbook_path)

    def test_get_writer(self):
        xlsx = initialize_workbook(self.workbook_path)
        self.assertIsInstance(xlsx.get_writer(), pd.ExcelWriter)
        xlsx.writer.close()
        cleanup_workbook(self.workbook_path)

    def test_get_workbook(self):
        xlsx = initialize_workbook(self.workbook_path)
        self.assertIsInstance(xlsx.workbook, xlsxwriter.workbook.Workbook)
        xlsx.writer.close()
        cleanup_workbook(self.workbook_path)

    def test_get_sheet(self):
        xlsx = initialize_workbook(self.workbook_path)
        self.assertIsNone(xlsx.get_sheet("SHEET_DOES_EXIST"))
        workbook = xlsx.get_workbook()
        workbook.add_worksheet("SHEET_DOES_EXIST")
        self.assertIsInstance(
            xlsx.get_sheet("SHEET_DOES_EXIST"), xlsxwriter.worksheet.Worksheet
        )
        xlsx.writer.close()
        cleanup_workbook(self.workbook_path)

    def test_generate_series(self):
        xlsx = initialize_workbook(self.workbook_path)

        xlsx.get_sheet("Sheet1")

        # generate series should return a dictionary object containing data + format information
        series = xlsx.generate_series(
            "Sheet1",
            2,
            1,
            10,
            line_style=None,
        )
        expected_result = {
            "categories": ["Sheet1", 1, 0, 10, 0],
            "marker": {"size": 5, "type": "circle"},
            "name": ["Sheet1", 0, 2],
            "smooth": True,
            "values": ["Sheet1", 1, 2, 10, 2],
        }
        self.assertEqual(series, expected_result)

        # test row_offset, smooth, line_style, marker_style props
        series = xlsx.generate_series(
            "Sheet1",
            2,
            21,
            30,
            marker_style={"type": "diamond", "size": 15},
            row_offset=1,
            smooth=False,
        )
        expected_result = {
            "categories": ["Sheet1", 21, 0, 30, 0],
            "line": {"width": 1},
            "marker": {"size": 15, "type": "diamond"},
            "name": ["Sheet1", 1, 2],
            "smooth": False,
            "values": ["Sheet1", 21, 2, 30, 2],
        }
        self.assertEqual(series, expected_result)

        # test col_category prop
        series = xlsx.generate_series(
            "Sheet1",
            3,
            1,
            10,
            col_category=1,
        )
        expected_result = {
            "categories": ["Sheet1", 1, 1, 10, 1],
            "line": {"width": 1},
            "marker": {"size": 5, "type": "circle"},
            "name": ["Sheet1", 0, 3],
            "smooth": True,
            "values": ["Sheet1", 1, 3, 10, 3],
        }
        self.assertEqual(series, expected_result)

        xlsx.writer.close()
        cleanup_workbook(self.workbook_path)

    def test_generate_reference_series(self):
        xlsx = initialize_workbook(self.workbook_path)

        xlsx.get_sheet("Sheet1")
        cals = pd.read_csv("tests/testdata_excelwriter_referencedata")

        # generate series should return a dictionary object containing data + format information
        series = xlsx.generate_reference_series(cals)
        self.assertEqual(series.get("name"), ["Events", 1, 2])
        self.assertEqual(series.get("values"), ["Events", 2, 2, 10, 2])
        self.assertEqual(series.get("categories"), ["Events", 2, 1, 10, 1])
        self.assertTrue(series.get("y2_axis"))

        # test relabel and row_offset props
        series = xlsx.generate_reference_series(cals, row_offset=5, relabel="NEW_NAME")
        self.assertEqual(series.get("name"), "NEW_NAME")
        self.assertEqual(series.get("values"), ["Events", 6, 2, 14, 2])
        self.assertEqual(series.get("categories"), ["Events", 6, 1, 14, 1])
        xlsx.writer.close()
        cleanup_workbook(self.workbook_path)

    def test_generate_timeseries_chart(self):
        p = PSenseParser()
        p.identify_file_source("tests/testdata_excelwriter_sensordata")
        p.load_rawfile("tests/testdata_excelwriter_sensordata", None, None)
        p.data.set_index("timestamp", inplace=True)

        xlsx = initialize_workbook(self.workbook_path)
        p.data.to_excel(xlsx.writer, sheet_name="Sheet1")
        xlsx.get_sheet("Sheet1")

        # check generating a chart with default settings
        chart = xlsx.generate_timeseries_chart(
            p.data,
            col_filter=["signal"],
            index_start=None,
            index_finish=None,
            y_range=None,
            chart_title="MY_TITLE",
            line_style={"width": 1},
            marker_style=None,
            second_axis=None,
        )
        # data has 3 channels: signal1, signal2, and signal3
        self.assertEqual(len(chart.series), 3)
        self.assertIsInstance(chart, xlsxwriter.chart_scatter.ChartScatter)
        # custom title
        self.assertEqual(chart.title_name, "MY_TITLE")
        # check ranges
        series = chart.series[0]
        self.assertEqual(series.get("categories"), "Sheet1!$A$2:$A$16")
        self.assertEqual(series.get("values"), "Sheet1!$B$2:$B$16")
        series = chart.series[1]
        self.assertEqual(series.get("categories"), "Sheet1!$A$2:$A$16")
        self.assertEqual(series.get("values"), "Sheet1!$F$2:$F$16")
        series = chart.series[2]
        self.assertEqual(series.get("values"), "Sheet1!$J$2:$J$16")
        self.assertEqual(chart.x_axis.get("name"), "timestamp")
        # check x-axis range is accurate
        self.assertEqual(
            convert_excelepoch_to_timestamp(chart.x_axis.get("min")), p.data.index[0]
        )
        self.assertEqual(
            convert_excelepoch_to_timestamp(chart.x_axis.get("max")), p.data.index[-1]
        )

        # check generating a chart
        chart = xlsx.generate_timeseries_chart(
            p.data,
            col_filter=["signal"],
            index_start=None,
            index_finish=None,
            y_range=None,
            chart_title="MY_TITLE",
            line_style={"width": 1},
            marker_style=None,
            second_axis=None,
            time_tick_nearest_hours=6,
        )
        # check x-axis range is accurate
        self.assertEqual(
            convert_excelepoch_to_timestamp(chart.x_axis.get("min")),
            p.data.index[0].floor("6 h"),
        )
        self.assertEqual(
            convert_excelepoch_to_timestamp(chart.x_axis.get("max")),
            p.data.index[-1].ceil("6 h"),
        )

        # check row subsets and axis ranges
        chart = xlsx.generate_timeseries_chart(
            p.data,
            col_filter=["vout"],
            index_start=5,
            index_finish=10,
            y_range=[0, 5],
            second_axis=[-100, 100],
        )
        # change column filter (search for vout* instead of signal*), check inputted offset + index subsets
        self.assertEqual(chart.series[0].get("values"), "Sheet1!$C$6:$C$11")
        self.assertEqual(chart.series[1].get("values"), "Sheet1!$G$6:$G$11")
        self.assertEqual(chart.series[2].get("values"), "Sheet1!$K$6:$K$11")
        # check modified axis ranges
        self.assertEqual(chart.y_axis.get("name"), "Sensor")
        self.assertEqual(chart.y_axis.get("min"), 0)
        self.assertEqual(chart.y_axis.get("max"), 5)
        self.assertEqual(chart.y2_axis.get("min"), -100)
        self.assertEqual(chart.y2_axis.get("max"), 100)

        # cleanup
        xlsx.writer.close()
        cleanup_workbook(self.workbook_path)

    def test_generate_calibration_chart(self):
        p = PSenseParser()
        p.identify_file_source("tests/testdata_excelwriter_sensordata")
        p.load_rawfile("tests/testdata_excelwriter_sensordata", None, None)
        p.data.set_index("timestamp", inplace=True)

        xlsx = initialize_workbook(self.workbook_path)
        p.data.to_excel(xlsx.writer, sheet_name="Sheet1")
        xlsx.get_sheet("Sheet1")

        cal = PSenseCalibration(
            expid="Sheet1",
            data=p.data,
            sample_offset_time=0,
            sample_window_time=1,
        )
        cal.add_reference(pd.Timestamp("2018-01-01 00:01:00"), 80)
        cal.add_reference(pd.Timestamp("2018-01-01 00:06:30"), 31)
        cal.calibration.set_index("ts", inplace=True)

        # generate a simple chart and check that the ranges are as-expected
        chart = xlsx.generate_calibration_chart(cal.calibration)
        self.assertEqual(chart.series[0].get("categories"), "Sheet1!$A$2:$A$3")
        self.assertEqual(chart.series[0].get("values"), "Sheet1!$B$2:$B$3")
        self.assertEqual(chart.series[1].get("values"), "Sheet1!$C$2:$C$3")
        self.assertEqual(chart.series[2].get("categories"), "Sheet1!$A$2:$A$3")
        self.assertEqual(chart.series[2].get("values"), "Sheet1!$D$2:$D$3")
        # default chart labels
        self.assertEqual(chart.y_axis.get("name"), "Sensor (nA)")
        self.assertEqual(chart.x_axis.get("name"), "Reference")
        # by default, each trace should have a trendline
        self.assertIsNotNone(chart.series[0].get("trendline"))
        self.assertIsNotNone(chart.series[1].get("trendline"))
        self.assertIsNotNone(chart.series[2].get("trendline"))

        # check offsets, labels, ranges, and trendline customizability
        chart = xlsx.generate_calibration_chart(
            cal.calibration,
            col_offset_ref=1,
            col_offset_sen=5,
            row_offset=1,
            y_label="MY_Y_LABEL",
            y_range=[-5, 5],
            x_label="MY_X_LABEL",
            x_range=[0, 100],
            trendline=None,
        )
        self.assertEqual(chart.series[0].get("categories"), "Sheet1!$B$3:$B$4")
        self.assertEqual(chart.series[0].get("values"), "Sheet1!$G$3:$G$4")
        self.assertEqual(chart.series[1].get("values"), "Sheet1!$H$3:$H$4")
        self.assertEqual(chart.series[2].get("categories"), "Sheet1!$B$3:$B$4")
        self.assertEqual(chart.series[2].get("values"), "Sheet1!$I$3:$I$4")
        # check custom x/y-axis settings
        self.assertEqual(chart.y_axis.get("name"), "MY_Y_LABEL")
        self.assertEqual(chart.x_axis.get("name"), "MY_X_LABEL")
        self.assertEqual(chart.y_axis.get("min"), -5)
        self.assertEqual(chart.x_axis.get("min"), 0)
        self.assertEqual(chart.y_axis.get("max"), 5)
        self.assertEqual(chart.x_axis.get("max"), 100)
        # disable trendline
        self.assertIsNone(chart.series[0].get("trendline"))


if __name__ == "__main__":
    unittest.main()
