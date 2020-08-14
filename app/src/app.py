import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly.graph_objs as go
import json
import os

import numpy as np

import sys

sys.path.append('/app/src')
from utilities.mzxml_functions import *
from style.plot_style import *

server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ]
)
app.config.suppress_callback_exceptions = False  # Formerly True to suppress

##### DEFINE STYLES #####
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# Load mzXML data
mzxml_in = '/app/data/toy.mzXML'
alldata = parse_mzxml_to_dataframe(mzxml_in)
global subdata


########## FILTER DEFINITION ##########
########## FILTER DEFINITION ##########
global filters
filters = dict()
filters['mzs'] = [alldata['mzs'].min(), alldata['mzs'].max()]
filters['rts'] = [alldata['rts'].min(), alldata['rts'].max()]
filters['its'] = [alldata['its'].min(), alldata['its'].max()]
########## FILTER DEFINITION END ######
########## FILTER DEFINITION END ######
# filters_const is a constant version of the data in the original dataframe
filters_const = filters.copy()
filters_const['mzs'] = [alldata['mzs'].min(),  alldata['mzs'].max()]
filters_const['rts'] = [alldata['rts'].min(),  alldata['rts'].max()]
filters_const['its'] = [alldata['its'].min(),  alldata['its'].max()]

def update_alldata_from_filters():
    return filter_dataframe(alldata, filters)

subdata = update_alldata_from_filters()

# DATA LOAD
def update_figure(subdata):
    z = np.linspace(0, 20, len(subdata))
    fig = go.Figure(data=[go.Scatter3d(
        x=subdata['rts'],
        y=subdata['mzs'],
        z=subdata['its'],
        mode='markers',
        marker=dict(
            size=2,
            color=z,  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            opacity=0.8
        )
    )]
    )
    # Define the plot labels
    fig.update_layout(scene=dict(
        xaxis_title='RetentionTime (h)',
        yaxis_title='m/z',
        zaxis_title='Intensity')
    )
    return fig



##### FIGURE CREATION #####
app.layout = html.Div(children=[
    html.H1(children='Data Visualization'),
    html.H5(children='File Input: ' + mzxml_in),
    html.Div(children=[
        html.Div(filter_intensity(filters['its'][0], filters['its'][1])),
        html.P('Intensity Range: [' + str(0) + ', ' + str(filters_const['its'][1]) + ']')
    ]),
    html.Div(children=[
        html.Div(filter_mz(filters['mzs'][0], filters['mzs'][1])),
        html.P('m/z Range: [' + str(filters_const['mzs'][0]) + ', '+ str(filters_const['mzs'][1]) +']')
    ]),
    html.Div(children=[
        html.Div(filter_retention_time(filters['rts'][0], filters['rts'][1])),
        html.P('RT Range (h): [' + str(filters_const['rts'][0]) + ', '+ str(filters_const['rts'][1]) +']')
    ]),
    html.Button('Update Graph', id='update_graph'),
    dcc.Graph(
        id='3d_mzxml_plot',
        figure=update_figure(subdata),
        style={'width': '100%', 'height': '90vh'}
    ),
    html.Div([
        dcc.Markdown("""
            **Click Data**
            Click on points in the graph.
        """),
        html.Pre(id='click-data', style=styles['pre']),
    ], className='three columns'),
])


########## DEFINE CALLBACKS ##########
########## DEFINE CALLBACKS ##########
@app.callback(
    Output('click-data', 'children'),
    [Input('3d_mzxml_plot', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('intensity_out', 'children'),
    [Input('intensity_min_filter', 'value'),
     Input('intensity_max_filter', 'value')
     ])
def update_intensity_out(intensity_out_min, intensity_out_max):
    filters['its'] = [intensity_out_min, intensity_out_max]
    return json.dumps(filters['its'])

@app.callback(
    Output('mz_out', 'children'),
    [Input('mz_min_filter', 'value'),
     Input('mz_max_filter', 'value')
     ])
def update_mz_out(mz_out_min, mz_out_max):
    filters['mzs'] = [mz_out_min, mz_out_max]
    return json.dumps(filters['mzs'])

@app.callback(
    Output('rt_out', 'children'),
    [Input('rt_min_filter', 'value'),
     Input('rt_max_filter', 'value')
     ])
def update_mz_out(rt_out_min, rt_out_max):
    filters['rts'] = [rt_out_min, rt_out_max]
    return json.dumps(filters['rts'])



@app.callback(
    Output('3d_mzxml_plot', 'figure'),
    [Input('update_graph', 'n_clicks')])
def update_graph(n_clicks):
    subdata = update_alldata_from_filters()
    fig = update_figure(subdata)
    return fig


if __name__ == '__main__':
    debug = False if os.environ['DASH_DEBUG_MODE'] == 'False' else True

    app.run_server(
        host='0.0.0.0',
        port=8050,
        debug=debug
    )
