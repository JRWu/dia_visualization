#!/usr/local/bin/python
from pyteomics import mass
import plotly.graph_objs as go


def fragments(peptide, types=('b', 'y'), maxcharge=1):
    """
    The function generates all possible m/z for fragments of types
    `types` and of charges from 1 to `maxharge`.
    Returns a dict of the b and y fragment ion s.
    """
    frgion_dict = {}
    for i in range(1, len(peptide) - 1):
        for ion_type in types:
            for charge in range(1, maxcharge + 1):
                if ion_type[0] in 'b':
                    bmass = mass.fast_mass(
                        peptide[:i], ion_type=ion_type, charge=charge)
                    frgion_dict['b' + str(i)] = bmass
                else:
                    ymass = mass.fast_mass(
                        peptide[i:], ion_type=ion_type, charge=charge)
                    frgion_dict['y' + str(i)] = ymass
    return frgion_dict


def generate_traces_from_frgions(frgions, trail_df_subset, fig):
    # Clear prior traces but keep the peaks.
    fig.data = [fig.data[0]]
    ppm = 10
    for key in frgions:
        frgion_df_tmp = trail_df_subset[
            (abs(frgions[key] - trail_df_subset['mzs'].astype(float)) / frgions[key] * 1000000) < ppm]
        if not frgion_df_tmp.empty:
            idx = frgion_df_tmp['row'].unique()[0]
            frgion_df_tmp = trail_df_subset[trail_df_subset['row'] == idx]
            frgion_df_tmp['rts'] = frgion_df_tmp['rts'].astype(float)
            frgion_df_tmp['mzs'] = frgion_df_tmp['mzs'].astype(float)
            frgion_df_tmp['ints'] = frgion_df_tmp['ints'].astype(float)
            frgion_df_tmp = frgion_df_tmp.sort_values(by='rts')
            fig.add_trace(
                go.Scatter3d(
                    x=frgion_df_tmp['rts'].astype(float),
                    y=frgion_df_tmp['mzs'].astype(float),
                    z=frgion_df_tmp['ints'].astype(float),
                    mode="lines",
                    text=key,
                    name=key
                )
            )
            fig['layout']['uirevision'] = 'STATIC'
    return fig
