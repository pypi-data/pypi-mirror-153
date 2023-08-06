from os import sep
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def parse_raw_df(df_hour_raw):
    columns_names = ["LOG_TIME", "LOG_TYPE", "PARTICIPANT_ID", "FILE_NAME", "NOTES"]
    df_burst_status = pd.DataFrame()
    df_dnd_status = pd.DataFrame()
    if df_hour_raw.shape[0] > 0:
        df_hour_raw.fillna('-1', inplace=True)
        df_burst_status = df_hour_raw
        df_dnd_status = df_hour_raw
        df_hour_raw.columns = columns_names
        df_hour_raw = df_hour_raw[~df_hour_raw["NOTES"].str.contains("Audio_profile")]

        # df_hour_raw['LOG_TIME'] = [x + " " + time_zone for x in df_hour_raw['LOG_TIME']]
        df_hour_raw[['SLEEP_OR_WAKE', 'SLEEP_OR_WAKE_TIME']] = df_hour_raw.NOTES.str.split("|", expand=True)
        df_hour_raw['SLEEP_OR_WAKE'] = df_hour_raw['SLEEP_OR_WAKE'].str.strip()
        df_hour_raw['SLEEP_OR_WAKE_TIME'] = df_hour_raw['SLEEP_OR_WAKE_TIME'].str.lstrip()
        df_hour_raw = df_hour_raw[(df_hour_raw['SLEEP_OR_WAKE'] == 'Current sleep time') |
                                  (df_hour_raw['SLEEP_OR_WAKE'] == 'Next wake time') |
                                  (df_hour_raw['SLEEP_OR_WAKE'] == 'Current wake time')]
        df_hour_raw = df_hour_raw.drop('LOG_TYPE', 1)
        df_hour_raw = df_hour_raw.drop('FILE_NAME', 1)
        df_hour_raw = df_hour_raw.drop('NOTES', 1)
        df_hour_raw = df_hour_raw[['PARTICIPANT_ID', 'LOG_TIME', 'SLEEP_OR_WAKE', 'SLEEP_OR_WAKE_TIME']]

        df_burst_status = df_burst_status[~df_burst_status["NOTES"].str.contains("Audio_profile")]
        df_burst_status[['DAY_TYPE', 'IS_BURST']] = df_burst_status.NOTES.str.split("|", expand=True)
        df_burst_status['DAY_TYPE'] = df_burst_status['DAY_TYPE'].str.strip()
        df_burst_status['IS_BURST'] = df_burst_status['IS_BURST'].str.strip()
        df_burst_status = df_burst_status[(df_burst_status['DAY_TYPE'] == 'BURST mode')]
        # print("No of rows:  " + str(df_burst_status.shape[0]))
        if df_burst_status.shape[0] != 0:
            df_burst_status = df_burst_status.drop('LOG_TYPE', 1)
            df_burst_status = df_burst_status.drop('FILE_NAME', 1)
            df_burst_status = df_burst_status.drop('NOTES', 1)
            df_burst_status = df_burst_status.drop('DAY_TYPE', 1)
            df_burst_status.loc[(df_burst_status.IS_BURST == 'true'), 'IS_BURST_DAY'] = 'True'
            df_burst_status.loc[(df_burst_status.IS_BURST == 'false'), 'IS_BURST_DAY'] = 'False'
            df_burst_status = df_burst_status.drop('IS_BURST', 1)
            df_burst_status = df_burst_status[['PARTICIPANT_ID', 'LOG_TIME', 'IS_BURST_DAY']]

        df_dnd_status = df_dnd_status[~df_dnd_status["NOTES"].str.contains("Audio_profile")]
        df_dnd_status[['DND', 'IS_DND']] = df_dnd_status.NOTES.str.split("|", expand=True)
        df_dnd_status['DND'] = df_dnd_status['DND'].str.strip()
        df_dnd_status['IS_DND'] = df_dnd_status['IS_DND'].str.strip()
        df_dnd_status = df_dnd_status[(df_dnd_status['DND'] == 'DND status')]
        if df_dnd_status.shape[0] != 0:
            df_dnd_status = df_dnd_status.drop('LOG_TYPE', 1)
            df_dnd_status = df_dnd_status.drop('FILE_NAME', 1)
            df_dnd_status = df_dnd_status.drop('NOTES', 1)
            df_dnd_status = df_dnd_status.drop('DND', 1)
            df_dnd_status.loc[(df_dnd_status.IS_DND == '1'), 'IS_IN_DND'] = 'False'
            df_dnd_status.loc[(df_dnd_status.IS_DND != '1'), 'IS_IN_DND'] = 'True'
            df_dnd_status = df_dnd_status.drop('IS_DND', 1)
            df_dnd_status = df_dnd_status[['PARTICIPANT_ID', 'LOG_TIME', 'IS_IN_DND']]
    return df_hour_raw, df_burst_status, df_dnd_status


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
