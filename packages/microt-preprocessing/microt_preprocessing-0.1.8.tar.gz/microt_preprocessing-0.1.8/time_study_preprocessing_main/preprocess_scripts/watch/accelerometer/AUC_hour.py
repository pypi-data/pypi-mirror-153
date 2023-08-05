from os import sep
import pandas as pd
import numpy as np
import warnings

# warnings.filterwarnings("ignore")
NAN = np.nan


def get_auc_matrix_hour(df_minute):
    ymd_list = []
    hour_list = []
    tz_list = []
    auc_sample_num_list = []
    auc_x_list = []
    auc_y_list = []
    auc_z_list = []

    ymd = list(df_minute.YEAR_MONTH_DAY.unique())[0]

    for hour in range(24):
        df_subset = df_minute[df_minute.HOUR == str(hour)]
        tz = list(df_subset.TIMEZONE.unique())[0]

        auc_sample_num_hour = df_subset.SAMPLE_COUNT.sum()
        if auc_sample_num_hour == 0:
            auc_x_hour = NAN
            auc_y_hour = NAN
            auc_z_hour = NAN
        else:
            auc_x_hour = df_subset.AUC_X.sum()
            auc_y_hour = df_subset.AUC_Y.sum()
            auc_z_hour = df_subset.AUC_Z.sum()

        ymd_list.append(ymd)
        hour_list.append(hour)
        tz_list.append(tz)
        auc_sample_num_list.append(auc_sample_num_hour)
        auc_x_list.append(auc_x_hour)
        auc_y_list.append(auc_y_hour)
        auc_z_list.append(auc_z_hour)

    df_hour = pd.DataFrame(
        {"YEAR_MONTH_DAY": ymd_list, "HOUR": hour_list, "TIMEZONE": tz_list, "SAMPLE_COUNT": auc_sample_num_list,
         "AUC_X": auc_x_list, "AUC_Y": auc_y_list, "AUC_Z": auc_z_list})

    return df_hour


if __name__ == "__main__":
    df_minute = pd.read_csv(
        r"C:\Users\Jixin\Downloads\auc_minute.csv")
    print(df_minute.TIMEZONE)
    df_hour = get_auc_matrix_hour(df_minute)
    print(df_hour)
    # df_hour.to_csv(r"C:\Users\Jixin\Downloads\watch_accelerometer_decompose_hour_2021-02-04.csv")
