import os
import atexit
import pandas as pd
import xlsxwriter


class ExcelWriter(object):
    "xlsxwriter wrapper with built-in generation of time-series and calibration charts (and series) for sensor data (expects PSenseParser formatted dataframes)"
    sheet_name: str = None
    writer: pd.ExcelWriter = None
    workbook: None

    def __init__(self, workbook_file):
        self.writer = pd.ExcelWriter(
            workbook_file,
            engine="xlsxwriter",
        )
        self.workbook = self.writer.book

    def get_writer(self):
        return self.writer

    def get_workbook(self):
        return self.workbook

    def get_sheet(self, sheet_name=None):
        if sheet_name:
            self.sheet_name = sheet_name

        return self.workbook.get_worksheet_by_name(self.sheet_name)

    def generate_series(
        self,
        sheet_name,
        col_value,
        row_min,
        row_max,
        line_style={"width": 1},
        marker_style={"type": "circle", "size": 5},
        col_category=0,
        smooth=True,
        row_offset=0,
    ):
        series_trace = {
            "name": [sheet_name, row_offset, col_value],
            "categories": [sheet_name, row_min, col_category, row_max, col_category],
            "values": [sheet_name, row_min, col_value, row_max, col_value],
            "smooth": smooth,
        }
        if line_style:
            series_trace["line"] = line_style
        if marker_style:
            series_trace["marker"] = marker_style
        return series_trace

    def generate_reference_series(
        self,
        df,
        marker_style={
            "type": "circle",
            "size": 7,
            "fill": {"color": "black"},
            "border": {"color": "black"},
        },
        row_offset=1,
        relabel=None,
    ):
        reference = self.generate_series(
            "Events",
            df.columns.get_loc("reference"),
            1 + row_offset,
            df.shape[0] + row_offset,
            row_offset=row_offset,
            line_style={"none": True},
            marker_style=marker_style,
            col_category=df.columns.get_loc("timestamp"),
        )

        if relabel:
            reference["name"] = relabel

        reference["y2_axis"] = True  # set this as a secondary axis trace
        return reference

    def generate_timeseries_chart(
        self,
        df,
        col_filter=["signal"],
        index_start=None,
        index_finish=None,
        y_range=None,
        chart_title=None,
        line_style={"width": 1},
        marker_style=None,
        second_axis=None,
        time_tick_nearest_hours=None,
        num_format="mm/dd HH:MM",
    ):
        # Create a chart object.
        chart = self.workbook.add_chart({"type": "scatter", "subtype": "smooth"})
        col_filter = [col_filter] if isinstance(col_filter, str) else col_filter

        # Configure the series of the chart from the dataframe data.
        row_min = index_start if index_start else 1
        row_max = index_finish if index_finish else df.shape[0]
        desired_columns = [
            df.columns.get_loc(column)
            for column in list(df.columns)
            if any(any_filter in column for any_filter in col_filter)
        ]
        for col_index in desired_columns:
            col = col_index + 1
            series_trace = self.generate_series(
                self.sheet_name, col, row_min, row_max, line_style, marker_style
            )
            chart.add_series(series_trace)

        # Configure the chart axes.
        x_style = {
            "name": "timestamp",
            "min": df.index[0]
            if not time_tick_nearest_hours
            else df.index[0].floor("{} h".format(time_tick_nearest_hours)),
            "max": df.index[-1]
            if not time_tick_nearest_hours
            else df.index[-1].ceil("{} h".format(time_tick_nearest_hours)),
            "date_axis": True,
            "num_format": num_format,
            # 'major_unit': 0.25,
        }
        y_style = {"name": "Sensor", "major_gridlines": {"visible": False}}
        if y_range:
            y_style["min"] = y_range[0]
            y_style["max"] = y_range[1]
            # if possible, shift axis to the bottom of the chart
            y_style["crossing"] = y_range[0]

        chart.set_x_axis(x_style)
        chart.set_y_axis(y_style)

        if second_axis:
            y_style = dict(name="Reference")
            if isinstance(second_axis, list):
                y_style["min"] = second_axis[0]
                y_style["max"] = second_axis[1]
            chart.set_y2_axis(y_style)

        chart.set_title({"name": chart_title if chart_title else self.sheet_name})
        return chart

    def generate_calibration_chart(
        self,
        cal,
        col_filter=["signal"],
        col_offset_ref=0,
        col_offset_sen=0,
        row_offset=0,
        y_label="Sensor (nA)",
        y_range=None,
        x_label="Reference",
        x_range=None,
        marker_style={"type": "automatic", "size": 5},
        trendline={
            "type": "linear",
            "display_equation": False,
            "display_r_squared": False,
        },
    ):
        chart = self.workbook.add_chart({"type": "scatter"})
        row_min = 1 + row_offset
        row_max = cal.shape[0] + row_offset
        col_reference_values = cal.columns.get_loc("ref") + col_offset_ref

        # Add regression values to the chart from the dataframe data.
        desired_columns = [
            cal.columns.get_loc(column)
            for column in list(cal)
            if any(any_filter in column for any_filter in col_filter)
        ]
        for col_index in desired_columns:
            col_data = col_index + col_offset_sen
            cal_trace = {
                "name": [self.sheet_name, row_offset, col_data],
                "categories": [
                    self.sheet_name,
                    row_min,
                    col_reference_values,
                    row_max,
                    col_reference_values,
                ],
                "values": [self.sheet_name, row_min, col_data, row_max, col_data],
                "marker": marker_style,
            }
            if trendline:
                cal_trace["trendline"] = trendline

            chart.add_series(cal_trace)

        # Configure the chart axes.
        x_style = dict(name=x_label)
        if x_range:
            x_style["min"] = x_range[0]
            x_style["max"] = x_range[1]
        chart.set_x_axis(x_style)

        y_style = dict(name=y_label)
        if y_range:
            y_style["min"] = y_range[0]
            y_style["max"] = y_range[1]
        chart.set_y_axis(y_style)

        return chart

    def atexit_cleanup(self):
        if not self.workbook.fileclosed:
            # self.workbook.save()
            self.writer.save()
