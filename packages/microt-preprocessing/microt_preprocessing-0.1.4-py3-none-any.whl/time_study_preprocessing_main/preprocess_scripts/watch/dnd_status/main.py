import csv
import os
import shutil
import sys
from os import path, makedirs
from ...utils.validate_dates import *
from ...utils.validate_hours import validate_hours
from .parse import *
import warnings
from shutil import copyfile

warnings.filterwarnings("ignore")

area = "logs-watch"
device = "watch"
file_shortname = "dnd_status"
target_file = "Watch-MiscLogger.log.csv"


def pre_process(microT_root_path, intermediate_file_save_path, p_id, date):
    participant_folder_path = microT_root_path
    area_folder_path = participant_folder_path + sep + area
    hours_with_target_file_list = {}  # included in participant stats report
    if path.exists(area_folder_path):
        date_folder_path = area_folder_path + sep + date
        if path.exists(date_folder_path):
            file_save_date_path = intermediate_file_save_path + sep + "intermediate_file" + sep + p_id + sep + date
            if not path.exists(file_save_date_path):
                makedirs(file_save_date_path)
            day_file_name = device + "_" + file_shortname + "_clean_" + date + ".csv"
            day_file_save_path = file_save_date_path + sep + day_file_name
            if not path.exists(day_file_save_path):
                df_participant = pd.DataFrame()
                validated_hour_list, HAVE_ALL_HOURS = validate_hours(date_folder_path)
                if len(validated_hour_list) == 0:
                    print("Cannot find hour folder in {} data".format(date))

                # iterate through hour folders
                hours_with_target_file = len(validated_hour_list)  # included in participant stats report
                for hour in validated_hour_list:
                    hour_folder_path = date_folder_path + sep + hour
                    target_file_path = hour_folder_path + sep + target_file

                    # step 2.1: read target hourly file
                    if target_file in listdir(hour_folder_path):
                        rows = []
                        with open(target_file_path) as resp_csv:
                            csv_reader = csv.reader(resp_csv, delimiter=",")
                            for row in csv_reader:
                                if len(row) == 4:
                                    rows.append(row)
                                # else:
                                #     print("warning: error line skipped    {}".format(target_file_path))
                        df_hour_raw = pd.DataFrame(rows)

                    else:
                        hours_with_target_file -= 1
                        continue

                    # step 2.2: parse target hourly file
                    # file_empty = False
                    if df_hour_raw.shape[0] != 0:
                        df_hour_parsed = parse_raw_df(df_hour_raw, p_id)
                        # step 2.4: concatenate hourly file in day level
                        if df_hour_parsed.shape[0] != 0:
                            df_participant = pd.concat([df_participant, df_hour_parsed])

                hours_with_target_file_list[date] = hours_with_target_file
                if hours_with_target_file != 0:
                    # step 3:  write out day file for participant
                    df_participant.to_csv(day_file_save_path, index=False)


if __name__ == "__main__":
    microT_root_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT"
    intermediate_file_save_path = r"C:\Users\jixin\Desktop\temp"
    p_id_list = ["aditya4_internal@timestudy_com"]
    date_start = "2020-01-01"
    date_end = "2020-07-01"
    hourKeep = True

    pre_process(microT_root_path, intermediate_file_save_path, p_id_list, date_start)
