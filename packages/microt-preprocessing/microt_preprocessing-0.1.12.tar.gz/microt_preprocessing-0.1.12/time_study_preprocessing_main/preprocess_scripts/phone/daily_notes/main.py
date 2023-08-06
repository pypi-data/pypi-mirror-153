import os
import shutil
from os import path, makedirs

from ...utils.validate_dates import *
from ...utils.validate_hours import validate_hours
from ...utils.get_time_zone import *
from .parse import *
import warnings
from shutil import copyfile

warnings.filterwarnings("ignore")

area = "logs"
device = "phone"
file_shortname = "daily_notes"
sleep_wake_notes = "sleep_wake"
burst_notes = "burst_status"
dnd_status = "dnd_status"

name_pattern = "MicroTUploadManagerServiceNotes"


def reg_exp_matching(hour_folder_path, name_pattern):
    file_list = listdir(hour_folder_path)
    matched_name = ""
    for file_str in file_list:
        if file_str.startswith(name_pattern):
            matched_name = file_str
            break
    return matched_name


def pre_process(microT_root_path, intermediate_file_save_path, p_id, decrypt_password, date):
    # copy_report_path = intermediate_file_save_path + sep + "intermediate_file" + sep + p_id
    # if not path.exists(copy_report_path):
    #     makedirs(copy_report_path)
    # p_id_no_domain = p_id.split("@")[0]
    # copied_report_file = copy_report_path + sep + p_id_no_domain + "_daily_report.csv"
    # original_report_file = microT_root_path + sep + p_id + sep + "reports" + sep + "report.csv"
    # if path.exists(original_report_file):
    #     copyfile(original_report_file, copied_report_file)
    # else:
    #     print("No report file found for: " + p_id)

    participant_folder_path = microT_root_path
    area_folder_path = participant_folder_path + sep + area
    hours_with_target_file_list = {}  # included in participant stats report
    if path.exists(area_folder_path):
        date_folder_path = area_folder_path + sep + date
        if path.exists(date_folder_path):
            file_save_date_path = intermediate_file_save_path + sep + "intermediate_file" + sep + p_id + sep + date
            if not path.exists(file_save_date_path):
                makedirs(file_save_date_path)
            day_file_name_sleep_wake = device + "_" + file_shortname + "_" + sleep_wake_notes + "_clean_" + date + ".csv"
            day_file_name_burst_status = device + "_" + file_shortname + "_" + burst_notes + "_clean_" + date + ".csv"
            day_file_name_dnd_status = device + "_" + file_shortname + "_" + dnd_status + "_clean_" + date + ".csv"

            day_file_save_path_sleep_wake = file_save_date_path + sep + day_file_name_sleep_wake
            day_file_save_path_burst = file_save_date_path + sep + day_file_name_burst_status
            day_file_save_path_dnd = file_save_date_path + sep + day_file_name_dnd_status

            if not path.exists(day_file_save_path_dnd) and not path.exists(
                    day_file_save_path_burst) and not path.exists(day_file_save_path_sleep_wake):
                df_pid_sleep_wake = pd.DataFrame()
                df_pid_burst_status = pd.DataFrame()
                df_pid_dnd_status = pd.DataFrame()

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
                            # print("Empty csv file", target_file_path)
                            continue
                    else:
                        hours_with_target_file -= 1
                        continue
                    # step 2.2: parse target hourly file

                    if df_hour_raw.shape[0] != 0:
                        df_hour_parsed, df_burst_status, df_dnd_status = parse_raw_df(df_hour_raw)
                        # step 2.4: concatenate hourly file in day level- only if the parsed dataframe is not empty
                        if df_hour_parsed.shape[0] != 0:
                            df_pid_sleep_wake = pd.concat([df_pid_sleep_wake, df_hour_parsed])

                        if df_burst_status.shape[0] != 0:
                            df_pid_burst_status = pd.concat([df_pid_burst_status, df_burst_status])

                        if df_dnd_status.shape[0] != 0:
                            df_pid_dnd_status = pd.concat([df_pid_dnd_status, df_dnd_status])

                hours_with_target_file_list[date] = hours_with_target_file

                if hours_with_target_file != 0:
                    df_pid_sleep_wake.to_csv(day_file_save_path_sleep_wake, index=False)

                    df_pid_burst_status.to_csv(day_file_save_path_burst, index=False)


if __name__ == "__main__":
    microT_root_path = r"C:\Users\jixin\Desktop\testing\logs"
    intermediate_file_save_path = r"C:\Users\jixin\Desktop\testing"
    p_id_list = ["rippingpeprepose@timestudy_com"]
    decrypt_password = ""
    date = "2021-11-17"

    pre_process(microT_root_path, intermediate_file_save_path, p_id, decrypt_password, date)
