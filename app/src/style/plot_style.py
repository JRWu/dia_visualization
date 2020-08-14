#!/usr/local/bin/python
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output


def filter_intensity(minval=0, maxval=100):
    return [
        dcc.Input(
            id="intensity_min_filter",
            type="number",
            debounce=True,
            placeholder="Min Intensity: " + str(minval),
            value=minval,
            min=minval
        ),
        dcc.Input(
            id="intensity_max_filter",
            type="number",
            debounce=True,
            placeholder="Max Intensity: " + str(maxval),
            value=maxval,
            max=maxval
        ),
        html.Div(id="intensity_out"),
    ]


def filter_mz(minval=0, maxval=100):
    return [
        dcc.Input(
            id="mz_min_filter",
            type="number",
            debounce=True,
            placeholder="Min m/z: " + str(minval),
            value=minval,
            min=minval
        ),
        dcc.Input(
            id="mz_max_filter",
            type="number",
            debounce=True,
            placeholder="Max m/z: " + str(maxval),
            value=maxval,
            max=maxval
        ),
        html.Div(id="mz_out"),
    ]


def filter_retention_time(minval=0, maxval=100):
    return [
        dcc.Input(
            id="rt_min_filter",
            type="number",
            debounce=True,
            placeholder="Min RT (h): " + str(minval),
            value=minval,
            min=minval
        ),
        dcc.Input(
            id="rt_max_filter",
            type="number",
            debounce=True,
            placeholder="Max RT (h): " + str(maxval),
            value=maxval,
            max=maxval
        ),
        html.Div(id="rt_out"),
    ]
