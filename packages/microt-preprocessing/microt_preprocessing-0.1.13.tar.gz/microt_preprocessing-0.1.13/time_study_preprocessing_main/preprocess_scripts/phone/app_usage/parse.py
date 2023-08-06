from os import sep
import pandas as pd
from ...utils.convert_timestamp import *
import warnings

warnings.filterwarnings("ignore")


def parse_raw_df(df_hour_raw, time_zone):
    columns_names = ["LOG_TIME", "LAST_HOUR_TIMESTAMP", "CURRENT_HOUR_TIMESTAMP", "APP_PACKAGE_NAME", "EVENT_TIMESTAMP",
                     "APP_EVENT"]
    if df_hour_raw.shape[0] > 0:
        df_hour_raw.fillna('-1', inplace=True)
        df_hour_raw.columns = columns_names
        df_hour_raw['LOG_TIME'] = [x + " " + time_zone for x in df_hour_raw['LOG_TIME']]
        df_hour_raw['LAST_HOUR_TIME'] = convert_timestamp_int_list_to_readable_time(df_hour_raw['LAST_HOUR_TIMESTAMP'],
                                                                                    time_zone)
        df_hour_raw['CURRENT_HOUR_TIME'] = convert_timestamp_int_list_to_readable_time(
            df_hour_raw['CURRENT_HOUR_TIMESTAMP'],
            time_zone)
        df_hour_raw['EVENT_TIME'] = convert_timestamp_int_list_to_readable_time(df_hour_raw['EVENT_TIMESTAMP'],
                                                                                time_zone)
        df_hour_raw = df_hour_raw[
            ["LOG_TIME", "LAST_HOUR_TIMESTAMP", 'LAST_HOUR_TIME', "CURRENT_HOUR_TIMESTAMP", 'CURRENT_HOUR_TIME',
             "APP_PACKAGE_NAME", "EVENT_TIMESTAMP", 'EVENT_TIME', "APP_EVENT"]]
    return df_hour_raw


if __name__ == "__main__":
    target_file = "Battery.020000000000-Battery.2020-06-02-02-00-25-506-M0400.event.csv"
    hour_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\data-watch\2020-06-02\02-EDT"
    target_file_path = hour_folder_path + sep + target_file
    output_file_path = r"C:\Users\jixin\Desktop\temp\temp_file.csv"
    p_id = "aditya4_internal@timestudy_com"

    df_hour_raw = pd.read_csv(target_file_path)
    print(df_hour_raw)
    df_hour_parsed = parse_raw_df(df_hour_raw)
    df_hour_parsed.to_csv(output_file_path, index=False)
