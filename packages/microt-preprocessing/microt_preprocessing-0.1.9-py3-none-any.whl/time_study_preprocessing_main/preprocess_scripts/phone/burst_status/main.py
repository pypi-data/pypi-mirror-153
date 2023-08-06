import os
import shutil
from os import path, makedirs

from ...utils.validate_dates import *
from ...utils.validate_hours import validate_hours
from ...utils.get_time_zone import *
from .parse import *
import warnings

warnings.filterwarnings("ignore")

area = "logs"
device = "phone"
file_shortname = "burst_status"

# since the battery file name is mixed with irregular numbers, file name matching is needed.
name_pattern = "MicroTUploadManagerServiceNotes"


def reg_exp_matching(hour_folder_path, name_pattern):
    file_list = listdir(hour_folder_path)
    matched_name = ""
    for file_str in file_list:
        if file_str.startswith(name_pattern):
            matched_name = file_str
            break
    return matched_name


def pre_process(microT_root_path, intermediate_file_save_path, p_id_list, decrypt_password, date_start, date_end, hourKeep):
    # for each participant
    for p_id in p_id_list:
        print("> Now processing {} file for {}  : ".format(name_pattern, p_id))
        participant_folder_path = microT_root_path + sep + p_id
        area_folder_path = participant_folder_path + sep + area
        if not path.exists(area_folder_path):
            print("Cannot find {} folder for participant {} .".format(area, p_id))
            continue

        # step 1: generate date range where date folder exists (sharable code in utils)
        validated_date_list = validate_dates(area_folder_path, date_start, date_end)
        if len(validated_date_list) == 0:
            print("Cannot find date folder in data source between {} and {}".format(date_start, date_end))
            continue

        days_with_all_hours = len(validated_date_list)  # included in participant stats report
        days_with_hours = len(validated_date_list)
        hours_with_target_file_list = {}  # included in participant stats report
        # step 2: iterate through all hour folders for each date
        for date in validated_date_list:
            df_participant = pd.DataFrame()
            date_folder_path = area_folder_path + sep + date
            file_save_date_path = intermediate_file_save_path + sep + "intermediate_file" + sep + p_id + sep + date
            if not path.exists(file_save_date_path):
                makedirs(file_save_date_path)
            temp_hourly_directory_path = file_save_date_path + sep + device + "_" + file_shortname + "_clean_hour_temp"

            # check hourly folder
            validated_hour_list, HAVE_ALL_HOURS = validate_hours(date_folder_path)
            if len(validated_hour_list) == 0:
                print("Cannot find hour folder in {} data".format(date))
                days_with_hours -= 1
                continue
            if not HAVE_ALL_HOURS:
                days_with_all_hours -= 1

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
                    df_hour_parsed = parse_raw_df(df_hour_raw)
                    # step 2.4: concatenate hourly file in day level
                    df_participant = pd.concat([df_participant, df_hour_parsed])

                # step 2.3: write out temp hourly preprocessed file (sharable code in utils)
                # if not path.exists(temp_hourly_directory_path):
                #     makedirs(temp_hourly_directory_path)
                # df_hour_parsed.to_csv(
                #     temp_hourly_directory_path + sep + device + "_" + file_shortname + "_clean_" + hour + ".csv",
                #     index=False)

            hours_with_target_file_list[date] = hours_with_target_file
            if hours_with_target_file != 0:
                # step 3:  write out day file for participant
                day_file_name = device + "_" + file_shortname + "_clean_" + date + ".csv"
                day_file_save_path = file_save_date_path + sep + day_file_name
                df_participant.to_csv(day_file_save_path, index=False)

            # step 4: delete hourly file
            # if not hourKeep:
            #     if os.path.isdir(temp_hourly_directory_path):
            #         shutil.rmtree(temp_hourly_directory_path)

        print("> total days with hour file for {} is {}".format(p_id, days_with_hours))
        print("> total hours file exist for {} is {}".format(p_id, sum(hours_with_target_file_list.values())))


if __name__ == "__main__":
    microT_root_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT"
    intermediate_file_save_path = r"C:\Users\jixin\Desktop\temp"
    p_id_list = ["aditya4_internal@timestudy_com"]
    date_start = "2020-01-01"
    date_end = "2020-07-01"

    pre_process(microT_root_path, intermediate_file_save_path, p_id_list, date_start, date_end)
