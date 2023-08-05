import os
import shutil
from os import path, makedirs

from ...utils.validate_dates import *
from ...utils.validate_hours import validate_hours
from ...utils.get_time_zone import *
from .parse import *
import warnings

warnings.filterwarnings("ignore")

area = "data"
device = "phone"
file_shortname = "ambient_press"
# since the battery file name is mixed with irregular numbers, file name matching is needed.
name_pattern = "AmbientPressManagerService"


def reg_exp_matching(hour_folder_path, name_pattern):
    file_list = listdir(hour_folder_path)
    matched_name = ""
    for file_str in file_list:
        if file_str.startswith(name_pattern):
            matched_name = file_str
            break
    return matched_name


def pre_process(microT_root_path, intermediate_file_save_path, p_id, decrypt_password, date):
    print("> Now processing {} file for {}  : ".format(name_pattern, p_id))
    participant_folder_path = microT_root_path
    area_folder_path = participant_folder_path + sep + area
    hours_with_target_file_list = {}  # included in participant stats report
    # step 2: iterate through all hour folders for each date
    if path.exists(area_folder_path):
        date_folder_path = area_folder_path + sep + date
        if path.exists(date_folder_path):
            df_participant = pd.DataFrame()
            file_save_date_path = intermediate_file_save_path + sep + "intermediate_file" + sep + p_id + sep + date
            day_file_name = device + "_" + file_shortname + "_clean_" + date + ".csv"
            day_file_save_path = file_save_date_path + sep + day_file_name
            temp_hourly_directory_path = file_save_date_path + sep + device + "_" + file_shortname + "_clean_hour_temp"


            # check hourly folder
            validated_hour_list, HAVE_ALL_HOURS = validate_hours(date_folder_path)
            if len(validated_hour_list) == 0:
                print("Cannot find hour folder in {} data".format(date))

            # iterate through hour folders
            hours_with_target_file = len(validated_hour_list)  # included in participant stats report
            for hour in validated_hour_list:
                hour_folder_path = date_folder_path + sep + hour

                # step 2.1: read target hourly file
                target_file_matched = reg_exp_matching(hour_folder_path, name_pattern)
                if len(target_file_matched) > 0:
                    target_file_path = hour_folder_path + sep + target_file_matched
                    try:
                        df_hour_raw = pd.read_csv(target_file_path, header=None)
                    except:
                        print("Empty csv file", target_file_path)
                        continue
                else:
                    hours_with_target_file -= 1
                    continue

                # step 2.2: parse target hourly file
                if df_hour_raw.shape[0] != 0:
                    # time zone
                    time_zone = get_time_zone(hour_folder_path)
                    df_hour_parsed = parse_raw_df(df_hour_raw, time_zone)
                    # step 2.4: concatenate hourly file in day level
                    df_participant = pd.concat([df_participant, df_hour_parsed])

            hours_with_target_file_list[date] = hours_with_target_file
            if hours_with_target_file != 0:
                # step 3:  write out day file for participant
                day_file_name = device + "_" + file_shortname + "_clean_" + date + ".csv"
                day_file_save_path = file_save_date_path + sep + day_file_name
                df_participant.to_csv(day_file_save_path, index=False)


if __name__ == "__main__":
    microT_root_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT"
    intermediate_file_save_path = r"C:\Users\jixin\Desktop\temp"
    p_id_list = ["aditya4_internal@timestudy_com"]
    date_start = "2020-01-01"
    date_end = "2020-07-01"

    pre_process(microT_root_path, intermediate_file_save_path, p_id_list, date_start, date_end)
