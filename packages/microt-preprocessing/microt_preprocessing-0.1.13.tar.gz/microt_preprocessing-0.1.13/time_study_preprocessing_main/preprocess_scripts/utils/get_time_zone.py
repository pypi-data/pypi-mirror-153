import os
from glob import glob

folder_list = ["data", "data-watch", "logs", "logs-watch"]


# def get_time_zone(date_folder_path):
#     time_zone = "unknownTZ"
#
#     if os.path.exists(date_folder_path):
#         hour_list = glob(os.path.join(date_folder_path, '*-*'))
#         for hour_path in hour_list:
#             time_zone = hour_path.split('-')[-1]
#             return time_zone
#
#     return time_zone

def get_time_zone(hour_folder_path):
    time_zone = "unknownTZ"

    if os.path.exists(hour_folder_path):
        time_zone = hour_folder_path.split('-')[-1]

    return time_zone


if __name__ == "__main__":
    p_id = "aditya4_internal@timestudy_com"
    date_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\data\2020-06-03"
    print("{} is located in time zone {} .".format(p_id, get_time_zone(date_folder_path)))
