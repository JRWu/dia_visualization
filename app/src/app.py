import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly.graph_objs as go

import numpy as np

import sys

sys.path.append('/app/src/utilities')
from mzxml_functions import *

server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ]
)
app.config.suppress_callback_exceptions = True

# Load mzXML data

from pyteomics import mzxml, auxiliary
import numpy as np
import pandas as pd

mzxml_in = '/app/data/toy.mzXML'

alldata = parse_mzxml_to_dataframe(mzxml_in)

# DATA LOAD
# Helix equation
# t = np.linspace(0, 20, 100)
# x, y, z = np.cos(t), np.sin(t), t
fig = go.Figure(data=[go.Scatter3d(
    x=alldata['rts'],
    y=alldata['mzs'],
    z=alldata['its'],
    mode='markers',
    marker=dict(
        size=2,
        #        color=z,                # set color to an array/list of desired values
        colorscale='Viridis',  # choose a colorscale
        opacity=0.8
    )
)])

fig.update_layout(scene=dict(
    xaxis_title='RetentionTime (h)',
    yaxis_title='m/z',
    zaxis_title='Intensity'),
    height=900
)

# FIGURE CREATION


app.layout = html.Div(children=[
    html.H1(children='Data Visualization'),

    html.Div(children='''
        Data Filter:
    '''),
    html.Div(id='container_col_select',
             children=dcc.Dropdown(id='col_select',
                                   options=[{
                                       'label': c.replace('_', ' ').title(),
                                       'value': c}
                                       for c in alldata.columns]),
             style={'display': 'inline-block', 'width': '30%', 'margin-left': '0%'}),
    dcc.Graph(
        id='mzXML overlay',
        figure=fig
    )
])

if __name__ == '__main__':
    import os

    debug = False if os.environ['DASH_DEBUG_MODE'] == 'False' else True

    app.run_server(
        host='0.0.0.0',
        port=8050,
        debug=debug
    )
