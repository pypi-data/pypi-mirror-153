from os import listdir
import re
from datetime import datetime, timedelta


def findExistedDateFolder(dates_list):
    existed_folder_list = [x for x in dates_list if bool(re.match(r'(\d+\-\d+\-\d+)', x))]
    return existed_folder_list


def filterDates(dates_list, date_start, date_end):
    dates_to_check = []
    date_format = '%Y-%m-%d'

    date_start_entered = datetime.strptime(date_start, date_format)
    date_end_entered = datetime.strptime(date_end, date_format)

    dt_dates = [datetime.strptime(date, date_format) for date in dates_list]
    dt_dates_sorted = sorted(dt_dates)

    for date in dt_dates_sorted:
        if (date >= date_start_entered) and (date <= date_end_entered):
            dates_to_check.append(date.strftime(date_format))

    return dates_to_check


def validate_dates(area_folder_path, date_start, date_end):
    dates_list = listdir(area_folder_path)
    if len(dates_list) == 0:
        return []

    dates_list_existed = findExistedDateFolder(dates_list)
    if len(dates_list_existed) == 0:
        return []

    dates_list_filtered = filterDates(dates_list_existed, date_start, date_end)
    if len(dates_list_filtered) > 0:
        validated_start_date = dates_list_filtered[0]
        validated_end_date = dates_list_filtered[-1]
    else:
        validated_start_date = "None"
        validated_end_date = "None"

    print("Entered Start Date (inclusive) :  {}   ,   Entered End Date (inclusive) :  {}".format(date_start, date_end))
    print("Validated Start Date (inclusive) :  {}   ,   Validated End Date (inclusive) :  {}".format(
        validated_start_date,
        validated_end_date))

    return dates_list_filtered


def get_relevant_date_list(folder_path, date_start, date_end):
    dates_list = listdir(folder_path)
    date_format = '%Y-%m-%d'
    date_start = datetime.strptime(date_start, date_format)
    date_end = datetime.strptime(date_end, date_format)
    if len(dates_list) == 0:
        return []
    dates_list_existed = findExistedDateFolder(dates_list)
    if len(dates_list_existed) == 0:
        return []
    formatted_dates = []
    for date in dates_list_existed:
        date = datetime.strptime(date, date_format)
        formatted_dates.append(date)
    min_date = min(formatted_dates)
    max_date = max(formatted_dates)
    if date_start <= min_date:
        date_start = min_date
    if date_end >= max_date:
        date_end = max_date
    final_dates = []
    date_increment = date_start
    while date_increment <= date_end:
        date_to_add = date_increment.strftime(date_format)
        final_dates.append(date_to_add)
        date_increment += timedelta(days=1)
    return final_dates


if __name__ == "__main__":
    area_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\logs-watch"
    date_start = "2020-01-01"
    date_end = "2020-07-01"

    validated_date_list = validate_dates(area_folder_path, date_start, date_end)
    print("Total number of valid date folders  :  {}".format(len(validated_date_list)))
    print(validated_date_list)
