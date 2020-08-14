#!/usr/local/bin/python

from pyteomics import mzxml, auxiliary
import numpy as np
import pandas as pd


def parse_mzxml_to_dataframe(mzxml_in):
    """
    Parse a mzXML file to a Pandas DataFrame.

    Args:
        mzxml_in: The mzXML file to be parsed.

    Return:
        Pandas DataFrame
    """

    # TODO: Add some error-handling here for file operations
    mzxml_iterator = mzxml.read(mzxml_in)

    all_rts = list()
    all_mzs = list()
    all_its = list()

    # Naively Iterate for each scan
    # TODO: In the future limit the number of scans for efficiency
    for scan in mzxml_iterator:
        scan_rt = scan['retentionTime']
        scan_mzs = scan['m/z array']
        scan_its = scan['intensity array']
        all_rts.append(np.repeat(scan_rt, len(scan_mzs)))
        all_mzs.append(scan_mzs)
        all_its.append(scan_its)

    # Unravel the list of arrays into a singular array
    rts = np.concatenate(all_rts).ravel()
    mzs = np.concatenate(all_mzs).ravel()
    its = np.concatenate(all_its).ravel()

    its = its/its.max()

    alldata = pd.DataFrame({
        'rts': rts,
        'mzs': mzs,
        'its': its
    })

    return alldata


def filter_dataframe(df, columns_minmax_dict):
    """
    Filter a given DataFrame based on the column:min_max values dict.

    Args:
        df: The DataFrame to be filtered.
        columns_minmax_dict: Dictionary with format column_name:[min_value, max_value] structure.

    Return:
        Subsetted Pandas DataFrame
    """

    subsetted_df = df
    # For each column to be filtered in the dictionary
    for column in columns_minmax_dict:
        minval = columns_minmax_dict[column][0]
        maxval = columns_minmax_dict[column][1]

        # Subset the respective column & values
        subsetted_df = subsetted_df.loc[(df[column] >= minval) & (subsetted_df[column] <= maxval)]
    return subsetted_df
