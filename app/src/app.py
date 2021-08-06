import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly.graph_objs as go
import sys
from pyteomics import mass
import numpy as np
import pandas as pd

sys.path.append('/app/src')
from utilities.mzxml_functions import *
from utilities.trail_functions import *
from style.plot_style import *
from utilities.peptide_functions import *
from utilities.xic_functions import *

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

##### Read in the XIC and Result files ...
iso_infile = '/app/data/isolationWindowRanges.out'
xic_infile = '/app/data/r01_q01_xic_experiment_xic.tsv'
res_infile = '/app/data/r01_q01_xic_experiment_result.tsv'
xic_data = pd.read_csv(xic_infile, sep='\t', header=0)
res_data = pd.read_csv(res_infile, sep="\t", header=0)

##### Read in ALL Trails
trail_dir = '/app/data/'
all_trails = dict()
for window_idx in range(1, 23):
    print(window_idx)
    all_trails[str(window_idx)] = (pd.read_table(trail_dir + str(window_idx) + '_window.tsv'))

##### Read in the Start/End Isolation Window m/z ranges
iso_dict = parse_isolation_windows(iso_infile)
rt_tolerance = 0.16

##### "Paginate" the first 10 values for easy loading
dropdown_startidx = 0
dropdown_endidx = 10
# Format the list of dropdown options
dropdown_options = list()
# Format the list of dropdown options
for index, row in res_data.iterrows():
    dropdown_options.append(
        {'label': row['peptide'], 'value': row['index']}
    )

# Define empty graph to be populated upon selection
fig = go.Figure(data=[])

app = dash.Dash()
app.layout = html.Div([
    html.H2(children='Trail + Peptide PSM Visualization'),
    dcc.Input(id="start_index", placeholder=dropdown_startidx, value=dropdown_startidx, debounce=True),
    dcc.Input(id="end_index", placeholder=dropdown_endidx, value=dropdown_endidx, debounce=True),
    dcc.Dropdown(
        id='dropdown_options',
        options=dropdown_options[dropdown_startidx:dropdown_endidx],
        value=dropdown_options[dropdown_startidx]['value']
    ),
    # html.Div(id='dropdown_output_container'),
    dcc.Graph(id="peak_scatterplot",
              figure=fig,
              style={'width': '100%', 'height': '100vh'}
              ),
])


########## CALLBACK DEFINITIONS ##########
@app.callback(
    Output(component_id='dropdown_options', component_property='options'),
    Input(component_id='start_index', component_property='value'),
    Input(component_id='end_index', component_property='value'),
)
def update_indicies(start_index, end_index):
    dropdown_startidx = int(start_index)
    dropdown_endidx = int(end_index)
    return dropdown_options[dropdown_startidx:dropdown_endidx]


@app.callback(
    dash.dependencies.Output('peak_scatterplot', 'figure'),
    [dash.dependencies.Input('dropdown_options', 'value')])
def update_output(value):
    # Plot the graph w/ trails here
    # Lookup the peptide from the dropdown options
    result_entry = list(filter(lambda x: x['value'] == value, dropdown_options))[0]
    # print(value)
    # print(result_entry)
    peptide_mass = float(mass.fast_mass(result_entry['label']))
    mz2 = (peptide_mass + 2 * 1.00727647) / 2
    iso_window = (np.max(np.where(np.array(list(iso_dict.keys())) < mz2)) + 1)
    res_row = res_data.loc[res_data['index'] == result_entry['value']]
    xic_row = xic_data.loc[res_data['index'] == result_entry['value']]
    rt_in = float(res_row['RT'])
    rt_tolerance = 0.16
    trail_df_subset = subset_trails_by_rt(all_trails[str(iso_window)], rt_in, rt_tolerance)
    trail_df_subset = subset_trails_by_rt(trail_df_subset, rt_in, rt_tolerance)
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
        uirevision='STATIC'
    ))
    """
        xaxis_range=[min(trail_df_subset['rts'].astype(float)), max(trail_df_subset['rts'].astype(float))],
        yaxis_range=[min(trail_df_subset['mzs'].astype(float)), max(trail_df_subset['mzs'].astype(float))],
        zaxis_range=[min(trail_df_subset['ints'].astype(float)), max(trail_df_subset['ints'].astype(float))],
        uirevision='STATIC'  # Prevent graph update
    ))
    """
    # return fig
    return generate_traces_from_json(xic_row, fig)


if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port=8050,
        debug=True,
        use_reloader=True
    )
