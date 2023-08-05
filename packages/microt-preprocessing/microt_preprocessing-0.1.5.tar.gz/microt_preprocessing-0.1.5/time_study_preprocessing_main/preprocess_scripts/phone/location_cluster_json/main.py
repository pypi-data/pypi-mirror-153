import os
import shutil
from os import path, makedirs

from ...utils.validate_dates import *
from ...utils.validate_hours import validate_hours
from .parse import *
import warnings
# import zipFile
import pyminizip

warnings.filterwarnings("ignore")

area = "data"
device = "phone"
file_shortname = "location_clustering_json"

# since the battery file name is mixed with irregular numbers, file name matching is needed.
name_pattern = "lsf.json"


def reg_exp_matching(hour_folder_path, name_pattern):
    file_list = listdir(hour_folder_path)
    matched_name = ""
    for file_str in file_list:
        if file_str.startswith(name_pattern):
            matched_name = file_str
            break
    return matched_name


def pre_process(microT_root_path, intermediate_file_save_path, p_id, decrypt_password, date):
    participant_folder_path = microT_root_path
    area_folder_path = participant_folder_path + sep + area

    # step 2: iterate through all hour folders for each date
    if path.exists(area_folder_path):
        date_folder_path = area_folder_path + sep + date
        if path.exists(date_folder_path):
            file_save_date_path = intermediate_file_save_path + sep + "intermediate_file" + sep + p_id + sep + date
            if not path.exists(file_save_date_path):
                makedirs(file_save_date_path)

            # check hourly folder
            validated_hour_list, HAVE_ALL_HOURS = validate_hours(date_folder_path)
            if len(validated_hour_list) == 0:
                print("Cannot find hour folders in {} data".format(date))
            # iterate through hour folders
            for hour in validated_hour_list:
                hour_folder_path = date_folder_path + sep + hour

                if not path.exists(hour_folder_path):
                    continue
                # step 2.1: read target hourly file
                target_file_matched = reg_exp_matching(hour_folder_path, name_pattern)

                if len(target_file_matched) > 0:
                    target_file_path = hour_folder_path + sep + target_file_matched
                    day_file_name = device + "_" + file_shortname + "_" + date + "_" + hour + ".json"
                    day_file_save_path = file_save_date_path + sep + day_file_name
                    day_zip_file_save_path = day_file_save_path + '.zip'
                    try:
                        pyminizip.compress(target_file_path, None, day_zip_file_save_path, decrypt_password, 0)
                    except:
                        # print("Empty csv file", target_file_path)
                        continue
                else:
                    continue


if __name__ == "__main__":
    microT_root_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT"
    intermediate_file_save_path = r"C:\Users\jixin\Desktop\temp"
    p_id_list = ["aditya4_internal@timestudy_com"]
    date_start = "2020-01-01"
    date_end = "2020-07-01"

    pre_process(microT_root_path, intermediate_file_save_path, p_id_list, date_start, date_end)
