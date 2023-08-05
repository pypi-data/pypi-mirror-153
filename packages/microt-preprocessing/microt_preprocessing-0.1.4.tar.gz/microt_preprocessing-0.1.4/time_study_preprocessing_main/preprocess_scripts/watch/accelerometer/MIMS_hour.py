from os import sep
import pandas as pd
import numpy as np
import warnings

# warnings.filterwarnings("ignore")
NAN = np.nan


def get_mims_matrix_hour(df_minute):
    ymd_list = []
    hour_list = []
    tz_list = []
    mims_sample_num_list = []
    mims_invalid_sample_num_list = []
    mims_sum_list = []

    ymd = list(df_minute.YEAR_MONTH_DAY.unique())[0]

    for hour in range(24):
        df_subset = df_minute[df_minute.HOUR == str(hour)]
        tz = list(df_subset.TIMEZONE.unique())[0]
        mims_sample_num_hour = df_subset.MIMS_SAMPLE_NUM.sum()
        if mims_sample_num_hour == 0:
            mims_invalid_sample_num_hour = NAN
            mims_sum_hour = NAN
        else:
            mims_invalid_sample_num_hour = df_subset.MIMS_INVALID_SAMPLE_NUM.sum()
            mims_sum_hour = df_subset.MIMS_SUM.sum()

        ymd_list.append(ymd)
        hour_list.append(hour)
        tz_list.append(tz)
        mims_sample_num_list.append(mims_sample_num_hour)
        mims_invalid_sample_num_list.append(mims_invalid_sample_num_hour)
        mims_sum_list.append(mims_sum_hour)

    df_hour = pd.DataFrame(
        {"YEAR_MONTH_DAY": ymd_list, "HOUR": hour_list, "TIMEZONE": tz_list, "MIMS_SAMPLE_NUM": mims_sample_num_list,
         "MIMS_INVALID_SAMPLE_NUM": mims_invalid_sample_num_list, "MIMS_SUM": mims_sum_list})

    return df_hour


if __name__ == "__main__":
    df_minute = pd.read_csv(
        r"C:\Users\Jixin\Downloads\watch_accelerometer_decompose_minute_2021-02-04.csv")
    df_hour = get_mims_matrix_hour(df_minute)
    print(df_hour)
    df_hour.to_csv(r"C:\Users\Jixin\Downloads\watch_accelerometer_decompose_hour_2021-02-04.csv")
