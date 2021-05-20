import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly.graph_objs as go
import sys

sys.path.append('/app/src')
from utilities.mzxml_functions import *
from utilities.trail_functions import *
from style.plot_style import *
from utilities.peptide_functions import *

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

trail_in = '/app/data/11_window.tsv'
trail_df = pd.read_table(trail_in)
target_rt = 19.6974904458599
rt_tolerance = 0.16

trail_df_subset = subset_trails_by_rt(trail_df, target_rt, rt_tolerance)
trail_df_subset = split_internal_columns(trail_df_subset)
trail_df_subset = trail_df_subset.apply(expand_lists, axis=1)
trail_df_subset = pd.concat(trail_df_subset.tolist())

fig = go.Figure(data=[go.Scatter3d(
    x=trail_df_subset['rts'].astype(float),
    y=trail_df_subset['mzs'].astype(float),
    z=trail_df_subset['ints'].astype(float),
    mode='markers',
    marker=dict(
        size=1.5,
        opacity=0.7
    ),
    showlegend=True,
    name="Peaks",
    uirevision='STATIC'  # Prevent graph update
)])
# Define the plot labels
fig.update_layout(scene=dict(
    xaxis_title='RetentionTime (min)',
    yaxis_title='m/z',
    zaxis_title='Intensity',
    xaxis_range=[min(trail_df_subset['rts'].astype(float)), max(trail_df_subset['rts'].astype(float))],
    yaxis_range=[min(trail_df_subset['mzs'].astype(float)), max(trail_df_subset['mzs'].astype(float))],
    zaxis_range=[min(trail_df_subset['ints'].astype(float)), max(trail_df_subset['ints'].astype(float))],
    uirevision='STATIC'  # Prevent graph update
))

##### Compute the Fragment Ion Traces here

global peptide_sequence
peptide_sequence = "SGGGGGGGGSSWGGR"
frgions = fragments(peptide_sequence)
generate_traces_from_frgions(frgions, trail_df_subset, fig)

##### Given some input peptide, we want to plot the PSM for each fragment ion & label it


app = dash.Dash()
app.layout = html.Div([
    html.H2(children='Trail + Peptide PSM Visualization'),
    dcc.Input(id="peptide_sequence", placeholder=peptide_sequence, value=peptide_sequence, debounce=True),
    html.Br(),
    dcc.Input(id="rt_in", placeholder=target_rt, value=target_rt, debounce=True),
    dcc.Graph(id="peak_scatterplot",
              figure=fig,
              style={'width': '100%', 'height': '100vh'}
              ),
    html.Div(id='my-output'),
])


########## CALLBACK DEFINITION ##########
@app.callback(
    Output(component_id='peak_scatterplot', component_property='figure'),
    Input(component_id='peptide_sequence', component_property='value'),
    Input(component_id='rt_in', component_property='value'),
)
def update_figure(peptide_sequence, rt_in):
    peptide_sequence = peptide_sequence
    rt_in = float(rt_in)
    trail_df_subset = subset_trails_by_rt(trail_df, rt_in, rt_tolerance)
    trail_df_subset = split_internal_columns(trail_df_subset)
    trail_df_subset = trail_df_subset.apply(expand_lists, axis=1)
    trail_df_subset = pd.concat(trail_df_subset.tolist())

    fig = go.Figure(data=[go.Scatter3d(
        x=trail_df_subset['rts'].astype(float),
        y=trail_df_subset['mzs'].astype(float),
        z=trail_df_subset['ints'].astype(float),
        mode='markers',
        marker=dict(
            size=1.5,
            opacity=0.7
        ),
        showlegend=True,
        name="Peaks",
        uirevision='STATIC'  # Prevent graph update
    )])
    fig.update_layout(scene=dict(
        xaxis_title='RetentionTime (min)',
        yaxis_title='m/z',
        zaxis_title='Intensity',
        xaxis_range=[min(trail_df_subset['rts'].astype(float)), max(trail_df_subset['rts'].astype(float))],
        yaxis_range=[min(trail_df_subset['mzs'].astype(float)), max(trail_df_subset['mzs'].astype(float))],
        zaxis_range=[min(trail_df_subset['ints'].astype(float)), max(trail_df_subset['ints'].astype(float))],
        uirevision='STATIC'  # Prevent graph update
    ))
    frgions = fragments(peptide_sequence)
    return generate_traces_from_frgions(frgions, trail_df_subset, fig)


"""
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
# **Click Data**
# Click on points in the graph.
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

"""

if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port=8050,
        debug=True,
        use_reloader=True
    )
