from os import sep
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def parse_raw_df(df_hour_raw, time_zone):
    columns_names = ["LOG_TIME", "LOG_TYPE", "PARTICIPANT_ID", "FILE_NAME", "LOG"]
    if df_hour_raw.shape[0] > 0:
        df_hour_raw.columns = columns_names
        df_hour_raw.fillna('-1', inplace=True)
        df_hour_raw = df_hour_raw[~df_hour_raw['LOG'].str.contains('TIME_TICK')]
        if (df_hour_raw.LOG == 'android.intent.action.SCREEN_ON').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.SCREEN_ON'), 'PHONE_EVENT'] = 'PHONE_SCREEN_ON'
        if (df_hour_raw.LOG == 'android.intent.action.SCREEN_OFF').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.SCREEN_OFF'), 'PHONE_EVENT'] = 'PHONE_SCREEN_OFF'
        if (df_hour_raw.LOG == 'android.intent.action.USER_PRESENT').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.USER_PRESENT'), 'PHONE_EVENT'] = 'PHONE_UNLOCKED'
        if (df_hour_raw.LOG == 'android.intent.action.BOOT_COMPLETED').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.BOOT_COMPLETED'), 'PHONE_EVENT'] = 'PHONE_BOOTED'
        if (df_hour_raw.LOG == 'android.intent.action.ACTION_SHUTDOWN').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.ACTION_SHUTDOWN'), 'PHONE_EVENT'] = 'PHONE_SHUTDOWN'
        if (df_hour_raw.LOG == 'android.intent.action.CONFIGURATION_CHANGED').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.CONFIGURATION_CHANGED'), 'PHONE_EVENT'] = \
            'PHONE_CONFIGRATION_CHANGED'
        if (df_hour_raw.LOG == 'android.intent.action.BATTERY_CHANGED').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.BATTERY_CHANGED'), 'PHONE_EVENT'] = \
            'PHONE_BATTERY_CHANGED'
        if (df_hour_raw.LOG == 'android.intent.action.ACTION_AIRPLANE_MODE_CHANGED').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.ACTION_AIRPLANE_MODE_CHANGED'), 'PHONE_EVENT'] = \
            'PHONE_AIRPLANE_MODE_CHANGED'
        if (df_hour_raw.LOG == 'android.intent.action.ACTION_USER_UNLOCKED').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.ACTION_USER_UNLOCKED'), 'PHONE_EVENT'] = \
            'PHONE_UNLOCKED'
        if (df_hour_raw.LOG == 'android.intent.action.HEADSET_PLUG').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.HEADSET_PLUG'), 'PHONE_EVENT'] = \
            'PHONE_HEADSET_PLUGGED'
        if (df_hour_raw.LOG == 'android.intent.action.ACTION_POWER_CONNECTED').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.ACTION_POWER_CONNECTED'), 'PHONE_EVENT'] = \
            'PHONE_POWER_CONNECTED'
        if (df_hour_raw.LOG == 'android.intent.action.ACTION_POWER_DISCONNECTED').shape[0] > 0:
            df_hour_raw.loc[(df_hour_raw.LOG == 'android.intent.action.ACTION_POWER_DISCONNECTED'), 'PHONE_EVENT'] = \
            'PHONE_POWER_DISCONNECTED'
        df_hour_raw = df_hour_raw.drop('LOG_TYPE', 1)
        df_hour_raw = df_hour_raw.drop('FILE_NAME', 1)
        df_hour_raw = df_hour_raw.drop('LOG', 1)
        if 'PHONE_EVENT' in df_hour_raw.columns:
            df_hour_raw = df_hour_raw[['PARTICIPANT_ID', 'LOG_TIME', 'PHONE_EVENT']]
        else:
            df_hour_raw = df_hour_raw[['PARTICIPANT_ID', 'LOG_TIME']]

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
