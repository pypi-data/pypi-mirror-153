import csv
import sys
import os
from glob import glob
import pandas as pd
from os import sep

# Import the rpy2 package to run R commands and then import MIMSunit package using that
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.robjects as ro
from rpy2.robjects import FloatVector
# pandas2ri.activate()


mims_unit = importr('MIMSunit')
get_mims = mims_unit.mims_unit

G_VAL = 9.8
DYNAMIC_RANGE = [-8, 8]


def csvToMIMS(hour_folder_path, date, hour):
    in_path = sorted(glob(os.path.join(hour_folder_path, '020000000000-AccelerationCalibrated.*.sensor.csv')))[0]

    # Read the csv file and create a data frame
    rows = []
    with open(in_path) as resp_csv:
        csv_reader = csv.reader(resp_csv, delimiter=",")
        for row in csv_reader:
            if len(row) > 3:
                rows.append(row)
            else:
                print("warning: error line skipped    {}".format(in_path))
    raw_data_csv = pd.DataFrame(rows[1:])
    raw_data_csv.columns = rows[0]

    raw_data_csv['X_ACCELATION_METERS_PER_SECOND_SQUARED'] = [float(x) / G_VAL for x in raw_data_csv['X_ACCELATION_METERS_PER_SECOND_SQUARED']]
    raw_data_csv['Y_ACCELATION_METERS_PER_SECOND_SQUARED'] = [float(x) / G_VAL for x in raw_data_csv['Y_ACCELATION_METERS_PER_SECOND_SQUARED']]
    raw_data_csv['Z_ACCELATION_METERS_PER_SECOND_SQUARED'] = [float(x) / G_VAL for x in raw_data_csv['Z_ACCELATION_METERS_PER_SECOND_SQUARED']]

    # Convert date to datetime object
    raw_data_csv['HEADER_TIME_STAMP'] = pd.to_datetime(raw_data_csv['HEADER_TIME_STAMP'], format='%Y-%m-%d %H:%M:%S.%f')

    # Convert to R dataframe needed for MIMSunit

    with localconverter(ro.default_converter + pandas2ri.converter):
        r_from_pd_df = ro.conversion.py2rpy(raw_data_csv)

    # r_from_pd_df = ro.conversion.py2rpy(raw_data_csv)

    # Convert dynamic range into R list
    r_g_range = FloatVector(DYNAMIC_RANGE)

    mims_df = get_mims(r_from_pd_df, dynamic_range=r_g_range, epoch='1 sec')


    with localconverter(ro.default_converter + pandas2ri.converter):
        pd_from_r_df = ro.conversion.rpy2py(mims_df)

    # pd_from_r_df = ro.conversion.rpy2py(mims_df)

    pd_from_r_df['HEADER_TIME_STAMP'] = pd_from_r_df['HEADER_TIME_STAMP'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # pd_from_r_df['HEADER_TIME_STAMP'] = pd_from_r_df['HEADER_TIME_STAMP'].apply(lambda x: x.replace(microsecond=0))
    out_path = os.path.dirname(in_path) + sep + "mims_" + date + "_" + hour + ".csv"
    pd_from_r_df.to_csv(out_path, index=False)
    return pd_from_r_df

if __name__ == "__main__":
    in_path = sys.argv[1]
    csvToMIMS(in_path)