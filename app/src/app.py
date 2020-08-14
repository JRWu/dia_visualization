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

from pyteomics import mzxml, auxiliary
import numpy as np
import pandas as pd 

mzxml_in = '/app/data/toy.mzXML'

all_rts = list()
all_mzs = list()
all_its = list()


# Iterate through every single scan and add the values to an index
mzxml_iterator = mzxml.read(mzxml_in)
scan = mzxml_iterator.next()

for scan in mzxml_iterator:
    # TODO: Iterate Here
    scan_rt = scan['retentionTime']
    scan_mzs = scan['m/z array']
    scan_its = scan['intensity array']
    all_rts.append(np.repeat(scan_rt,len(scan_mzs)))
    all_mzs.append(scan_mzs)
    all_its.append(scan_its)

rts = np.concatenate(all_rts).ravel()   # X-Axis
mzs = np.concatenate(all_mzs).ravel()   # Y-Axis
its = np.concatenate(all_its).ravel()   # Z-Axis

alldata = pd.DataFrame({
    'rts': rts,
    'mzs': mzs,
    'its': its
})




# DATA LOAD 
# Helix equation
#t = np.linspace(0, 20, 100)
#x, y, z = np.cos(t), np.sin(t), t
fig = go.Figure(data=[go.Scatter3d(
    x=alldata['rts'],
    y=alldata['mzs'],
    z=alldata['its'],
    mode='markers',
    marker=dict(
        size=2,
#        color=z,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)])

fig.update_layout(scene = dict(
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