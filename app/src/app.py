import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask

import plotly.graph_objs as go


import numpy as np


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



# DATA LOAD 
# Helix equation
t = np.linspace(0, 20, 100)
x, y, z = np.cos(t), np.sin(t), t
fig = go.Figure(data=[go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=12,
        color=z,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)])
# FIGURE CREATION


app.layout = html.Div(children=[
    html.H1(children='Data Visualization'),

    html.Div(children='''
        DIA Visualization Dataset
    '''),
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