from os import sep
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def parse_raw_df(df_hour_raw):
    columns_names = ["LOG_TIME", "LOG_TYPE", "PARTICIPANT_ID", "FILE_NAME", "LOG"]
    if df_hour_raw.shape[0] > 0:
        df_hour_raw.columns = columns_names
        selected_idxes = []
        for idx in df_hour_raw.index:
            if "Ringer Mode" in str(df_hour_raw['LOG'][idx]):
                selected_idxes.append(idx)

        df_hour_raw = df_hour_raw.iloc[selected_idxes]

        df_hour_raw = df_hour_raw.drop('LOG_TYPE', 1)
        df_hour_raw = df_hour_raw.drop('FILE_NAME', 1)
        df_hour_raw.reset_index(inplace=True, drop=True)

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
