from os import sep
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def parse_raw_df(df_hour_raw, time_zone):
    columns_names = ["LOG_TIME", "LOG_TYPE", "PARTICIPANT_ID", "FILE_NAME", "LOG"]
    if df_hour_raw.shape[0] > 0:
        df_hour_raw.columns = columns_names
        df_hour_raw.fillna('-1', inplace=True)
        df_hour_raw['LOG_TIME'] = [x + " " + time_zone for x in df_hour_raw['LOG_TIME']]
        df_hour_raw = df_hour_raw[df_hour_raw['LOG'].str.contains('Wifi state')]
        if df_hour_raw.LOG.size > 0:
            df_hour_raw[['WIFI', 'WIFI_BOOL']] = df_hour_raw.LOG.str.split(":", expand=True)
            df_hour_raw['WIFI_BOOL'] = df_hour_raw['WIFI_BOOL'].str.strip()
            df_hour_raw.loc[(df_hour_raw.WIFI_BOOL == 'true'), 'IS_WIFI_ON'] = 'True'
            df_hour_raw.loc[(df_hour_raw.WIFI_BOOL == 'false'), 'IS_WIFI_ON'] = 'False'
            df_hour_raw = df_hour_raw.drop('LOG_TYPE', 1)
            df_hour_raw = df_hour_raw.drop('FILE_NAME', 1)
            df_hour_raw = df_hour_raw.drop('LOG', 1)
            df_hour_raw = df_hour_raw.drop('WIFI', 1)
            df_hour_raw = df_hour_raw.drop('WIFI_BOOL', 1)
            df_hour_raw = df_hour_raw[
                ['PARTICIPANT_ID', 'LOG_TIME', 'IS_WIFI_ON']]
    return df_hour_raw


if __name__ == "__main__":
    target_file = "Battery.020000000000-Battery.2020-06-02-02-00-25-506-M0400.event.csv"
    hour_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\data-watch\2020-06-02\02-EDT"
    target_file_path = hour_folder_path + sep + target_file
    output_file_path = r"C:\Users\jixin\Desktop\temp\temp_file.csv"
    p_id = "aditya4_internal@timestudy_com"

    df_hour_raw = pd.read_csv(target_file_path)
    # print(df_hour_raw)
    df_hour_parsed = parse_raw_df(df_hour_raw)
    df_hour_parsed.to_csv(output_file_path, index = False)
