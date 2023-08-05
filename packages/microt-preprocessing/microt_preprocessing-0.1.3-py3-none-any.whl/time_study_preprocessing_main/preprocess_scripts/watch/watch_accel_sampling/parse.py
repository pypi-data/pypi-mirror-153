import pandas as pd
import os
from os import sep
from ...utils.convert_timestamp import *
import warnings

warnings.filterwarnings("ignore")


def parse_raw_df(df_hour_raw, p_id, time_zone):
    if df_hour_raw.shape[0] != 0:
        df_hour_raw.fillna(-1, inplace=True)
        column_names = ['LOG_TIME', 'LOG_TYPE', 'WINDOW_START_TIMESTAMP', 'NUM_SAMPLES',
                        'AUC_X', 'AUC_Y',
                        'AUC_Z']
        df_hour_raw.columns = column_names
        df_hour_raw.insert(0, 'PARTICIPANT_ID', p_id)
        df_hour_raw = df_hour_raw.drop('LOG_TYPE', 1)
        df_hour_raw['WINDOW_START_TIME'] = convert_timestamp_int_list_to_readable_time(df_hour_raw['WINDOW_START_TIMESTAMP'],
                                                                                       time_zone)
        df_hour_raw = df_hour_raw[
            ['PARTICIPANT_ID', 'LOG_TIME', 'WINDOW_START_TIMESTAMP', 'WINDOW_START_TIME',
             'NUM_SAMPLES', 'AUC_X', 'AUC_Y', 'AUC_Z']]
    return df_hour_raw


if __name__ == "__main__":
    target_file = "Watch-AccelSampling.log.csv"
    hour_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\logs-watch\2020-05-31\10-EDT"
    target_file_path = hour_folder_path + sep + target_file
    output_file_path = r"C:\Users\jixin\Desktop\temp\temp_file.csv"
    p_id = "aditya4_internal@timestudy_com"

    df_hour_raw = pd.read_csv(target_file_path, header=None)
    df_hour_parsed = parse_raw_df(df_hour_raw, p_id)
    df_hour_parsed.to_csv(output_file_path, index=False)
