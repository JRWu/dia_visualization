#!/usr/local/bin/python

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import json

def generate_traces_from_json(xic_row, fig):
    # Clear prior traces but keep the peaks.
    fig.data = [fig.data[0]]
    deserialized_xic = json.loads(xic_row["xic"].iloc[0])
    for b_ion in deserialized_xic['b']:
        if len(deserialized_xic['b'][str(b_ion)]) > 0:
            # rts
            x = pd.Series(list(dict.keys(deserialized_xic['b'][str(b_ion)]))).astype(float)
            y = pd.Series(
                [deserialized_xic['bMZ'][str(b_ion)]] * len(list(dict.keys(deserialized_xic['b'][str(b_ion)]))))
            z = pd.Series(list(dict.values(deserialized_xic['b'][str(b_ion)]))).astype(float)
            xic_df = pd.DataFrame({'rts': x, 'mzs': y, 'ints': z})
            xic_df = xic_df.sort_values(by='rts')
            fig.add_trace(
                go.Scatter3d(
                    x=xic_df['rts'].astype(float),
                    y=xic_df['mzs'].astype(float),
                    z=xic_df['ints'].astype(float),
                    mode="lines",
                    text='b' + str(b_ion),
                    name='b' + str(b_ion)
                )
            )
    for y_ion in deserialized_xic['y']:
        if len(deserialized_xic['y'][str(y_ion)]) > 0:
            # rts
            x = pd.Series(list(dict.keys(deserialized_xic['y'][str(y_ion)]))).astype(float)
            y = pd.Series(
                [deserialized_xic['yMZ'][str(y_ion)]] * len(list(dict.keys(deserialized_xic['y'][str(y_ion)]))))
            z = pd.Series(list(dict.values(deserialized_xic['y'][str(y_ion)]))).astype(float)
            xic_df = pd.DataFrame({'rts': x, 'mzs': y, 'ints': z})
            xic_df = xic_df.sort_values(by='rts')
            fig.add_trace(
                go.Scatter3d(
                    x=xic_df['rts'].astype(float),
                    y=xic_df['mzs'].astype(float),
                    z=xic_df['ints'].astype(float),
                    mode="lines",
                    text='y' + str(y_ion),
                    name='y' + str(y_ion)
                )
            )
    fig['layout']['uirevision'] = 'STATIC'
    return fig
