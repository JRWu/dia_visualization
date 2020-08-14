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

    alldata = pd.DataFrame({
        'rts': rts,
        'mzs': mzs,
        'its': its
    })

    return alldata
