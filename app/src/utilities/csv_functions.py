#!/usr/local/bin/python

import pandas as pd

def parse_diaumpire_csv_into_plottable_traces(csv_infile):
    csv_df = pd.read_csv(csv_infile)

    mzcols = ['mz1', 'mz2', 'mz3', 'mz4']
    rtcols = ['PeakHeightRT1', 'PeakHeightRT2', 'PeakHeightRT3', 'PeakHeightRT4']
    itcols = ['PeakHeight1', 'PeakHeight2', 'PeakHeight3', 'PeakHeight4']

    x_lines = list()
    y_lines = list()
    z_lines = list()

    for index, row in csv_df.iterrows():
        extracted = row[mzcols + rtcols + itcols]
        extracted = extracted.values.reshape(3, 4).T
        # RTs
        x_lines.extend(extracted[:, 0][extracted[:, 0] != 0])
        x_lines.append(None)

        # MZs
        y_lines.extend(extracted[:, 1][extracted[:, 1] != 0])
        y_lines.append(None)

        # ITs
        z_lines.extend(extracted[:, 2][extracted[:, 2] != 0])
        z_lines.append(None)

    return (x_lines, y_lines, z_lines)
