from os import listdir, sep
import re


def findExistedHourFolder(hours_list):
    existed_folder_list = [x for x in hours_list if bool(re.match(r'\d{2}-[A-Z]{3}(\+[0-9_]{5}|$)', x))
                           or bool(re.match(r'\d{2}-[A-Z]{4}(\+[0-9_]{5}|$)', x))
                           or bool(re.match(r'\d{2}-[A-Z]{3}-\d{4}(\+[0-9_]{5}|$)', x))
                           or bool(re.match(r'\d{2}-[A-Z]{3}(-|\+)\d{2}:\d{2}', x))
                           or bool(re.match(r'\d{2}-[A-Z]{3}_\d+', x))
                           ]
    return existed_folder_list


def validate_hours(date_folder_path):
    hours_list = listdir(date_folder_path)
    if len(hours_list) == 0:
        return []

    hours_list_existed = findExistedHourFolder(hours_list)

    HAVE_ALL_HOURS = True
    if len(hours_list_existed) != 24:
        HAVE_ALL_HOURS = False

    return hours_list_existed, HAVE_ALL_HOURS


if __name__ == "__main__":
    area_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\logs-watch"
    date = listdir(area_folder_path)[1]
    date_folder_path = area_folder_path + sep + date

    validated_hour_list, HAVE_ALL_HOURS = validate_hours(date_folder_path)
    print(date)
    print("Total number of valid hour folders  :  {}".format(len(validated_hour_list)))
    print("Does the date have 24 hour folders : {}".format(HAVE_ALL_HOURS))
    print(validated_hour_list)
