from os import path, sep
from glob import glob
import pandas as pd


# How this works: search through the intermediate save folder
def generate_output_report(microT_root_path, intermediate_file_save_path, current_date):
    info_list_phone = ["phone_app_usage", "phone_apps_usage_duration", "phone_battery", "phone_daily_notes_burst_status",
                       "phone_daily_notes_dnd_status", "phone_daily_notes_sleep_wake", "phone_detected_activity",
                       "phone_GPS*.csv.zip", "phone_notifications", "phone_system_events", "phone_promptresponse",
                       "phone_stepCount", "phone_wifi_state", "phone_apps_installed"]

    info_list_watch = ["watch_promptresponse", "watch_battery", "watch_accelsampling", "watch_dnd_status",
                       "watch_power_status", "watch_uema_undo_counts", "watch_accelerometer_har_*activity",
                       "watch_accelerometer_har_*intensity", "watch_accelerometer_har_*posture",
                       "watch_accelerometer_mims", "watch_accelerometer_swan"]

    all_info_list = info_list_phone + info_list_watch
    all_columns_list = ["Participant", "Date"] + all_info_list
    # column_num = len(all_info_list)

    root_path_components = microT_root_path.split(sep)
    p_id = root_path_components[len(root_path_components) - 1]

    participant_save_folder_path = intermediate_file_save_path + sep + "intermediate_file" + sep + p_id
    participant_date_folder_path = participant_save_folder_path + sep + current_date

    file_exists_list = [p_id, current_date]

    print(participant_date_folder_path)
    if path.exists(participant_date_folder_path):
        for info in all_info_list:
            filter_list = list(glob(participant_date_folder_path + sep + info + "*"))
            if len(filter_list) == 1:
                file_exists_list.append(True)
            else:
                file_exists_list.append(False)
        summary_df = pd.DataFrame(data=[file_exists_list], columns=all_columns_list)
        summary_df.to_csv(participant_date_folder_path + sep + "intermedaite_output_summary_report.csv", index=False)
        print("Generate output summary file successfully!")

    return

