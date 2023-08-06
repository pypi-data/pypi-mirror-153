from os import sep
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def parse_raw_df(df_hour_raw, time_zone):
    columns_names = ["LOG_TIME", "APP_PACKAGE_NAME", "APP_VERSION_CODE", "APP_VERSION_NAME"]
    if df_hour_raw.shape[0] > 0:
        df_hour_raw.fillna('-1', inplace=True)
        df_hour_raw.columns = columns_names
        df_hour_raw['LOG_TIME'] = [x + " " + time_zone for x in df_hour_raw['LOG_TIME']]
    return df_hour_raw


if __name__ == "__main__":
    target_file = "MicroTUploadManagerServiceNotes.log.csv"
    hour_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\data-watch\2020-06-02\02-EDT"
    target_file_path = hour_folder_path + sep + target_file
    output_file_path = r"C:\Users\jixin\Desktop\temp\temp_file.csv"
    p_id = "aditya4_internal@timestudy_com"

    df_hour_raw = pd.read_csv(target_file_path)
    print(df_hour_raw)
    df_hour_parsed = parse_raw_df(df_hour_raw)
    df_hour_parsed.to_csv(output_file_path, index=False)
