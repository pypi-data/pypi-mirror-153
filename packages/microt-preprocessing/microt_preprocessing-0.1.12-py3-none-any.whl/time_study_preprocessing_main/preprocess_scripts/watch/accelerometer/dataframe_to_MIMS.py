import csv
import sys
import os
from glob import glob
import pandas as pd
from os import sep, path

# Import the rpy2 package to run R commands and then import MIMSunit package using that
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.robjects as ro
from rpy2.robjects import FloatVector
import warnings

warnings.filterwarnings("ignore")

mims_unit = importr('MIMSunit')
feather_r = importr('arrow')
get_mims = mims_unit.mims_unit

G_VAL = 9.8
DYNAMIC_RANGE = [-8, 8]


def dataframe_to_MIMS(hour_folder_path, date, hour, df):
    in_path = hour_folder_path
    out_har_path = hour_folder_path + sep + "har_" + date + "_" + hour + ".csv"

    raw_data_csv = df

    # Convert to R dataframe needed for MIMSunit
    feather_path = hour_folder_path + sep + 'temp_feather.feather'
    print("Feather file at: " + feather_path)
    raw_data_csv.to_feather(feather_path)
    if path.exists(feather_path):
        r_from_pd_df = feather_r.read_feather(feather_path)
    if path.exists(feather_path):
        os.remove(feather_path)
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     r_from_pd_df = ro.conversion.py2rpy(raw_data_csv)
    # Convert dynamic range into R list
    r_g_range = FloatVector(DYNAMIC_RANGE)
    mims_df = get_mims(r_from_pd_df, dynamic_range=r_g_range, epoch='1 sec')
    with localconverter(ro.default_converter + pandas2ri.converter):
        pd_from_r_df = ro.conversion.rpy2py(mims_df)

    pd_from_r_df['HEADER_TIME_STAMP'] = pd_from_r_df['HEADER_TIME_STAMP'].dt.strftime('%Y-%m-%d %H:%M:%S')
    out_path = in_path + sep + "mims_" + date + "_" + hour + ".csv"
    pd_from_r_df.to_csv(out_path, index=False)
    return pd_from_r_df


if __name__ == "__main__":
    in_path = sys.argv[1]
    dataframe_to_MIMS(in_path)
