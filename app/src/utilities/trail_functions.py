#!/usr/local/bin/python
import pandas as pd

#trail_infile = "/app/data/11_window.tsv"
#trail_df = pd.read_table(trail_infile)

#target_rt = 20.0
#rt_tolerance = 0.16


def subset_trails_by_rt(trail_df, target_rt, rt_tolerance):
    upper_rt = target_rt + rt_tolerance
    lower_rt = target_rt - rt_tolerance
    return trail_df[(trail_df["maxRT"] < upper_rt) & (trail_df["maxRT"] > lower_rt)]


#trail_df_subset = subset_trails_by_rt(trail_df, target_rt, rt_tolerance)

def tokenize_column_by_comma(column_value):
    return list(filter(None, column_value.split(",")))

def split_internal_columns(trail_df):
    trail_df["split_rts"] = trail_df["rts"].apply(tokenize_column_by_comma)
    trail_df["split_ints"] = trail_df["ints"].apply(tokenize_column_by_comma)
    trail_df["split_mzs"] = trail_df["mzs"].apply(tokenize_column_by_comma)
    return trail_df

"""
# list(filter(None, trail_df_subset.iloc[0]["ints"].split(",")))
trail_df_subset["split_rts"] = trail_df_subset["rts"].apply(tokenize_column_by_comma)
trail_df_subset["split_ints"] = trail_df_subset["ints"].apply(tokenize_column_by_comma)
trail_df_subset["split_mzs"] = trail_df_subset["mzs"].apply(tokenize_column_by_comma)
"""
def expand_lists(row):
    expanded_df = pd.DataFrame(
        list(
            zip(row["split_rts"], row["split_ints"],
                row["split_mzs"],
                [getattr(row, "name")] * len(row["split_rts"])))
        , columns=["rts", "ints", "mzs", "row"]
    )
    return expanded_df

"""
expanded_df = trail_df_subset.apply(expand_lists, axis=1)
indexed_trail_df = pd.concat(expanded_df.tolist())
"""

