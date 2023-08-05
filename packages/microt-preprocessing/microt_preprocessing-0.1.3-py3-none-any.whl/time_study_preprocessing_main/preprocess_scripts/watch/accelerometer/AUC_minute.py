from os import sep
import pandas as pd
import numpy as np
import warnings

# warnings.filterwarnings("ignore")
NAN = np.nan
colnames = ["YEAR_MONTH_DAY", "HOUR", "MINUTE", "TIMEZONE", "SAMPLE_COUNT",	"AUC_X", "AUC_Y", "AUC_Z"]

from datetime import datetime, timedelta
import pandas as pd

time_offset_dict = {
    "CDT": "UTC-05",
    "CST": "UTC-06",
    "MDT": "UTC-06",
    "MST": "UTC-07",
    "PDT": "UTC-07",
    "PST": "UTC-08",
    "EDT": "UTC-04",
    "EST": "UTC-05",
    "AKDT": "UTC-08",
    "AKST": "UTC-09",
    "HDT": "UTC-09",
    "HST": "UTC-10"
}


def parse_time_offset(time_offset):
    sign_str = time_offset.strip('UTC')[0]
    if sign_str == "-":
        sign = -1
    elif sign_str == "+":
        sign = 1
    else:
        sigh = 0

    time_offset_int = int(time_offset.strip('UTC')[1:])
    time_delta = timedelta(hours=time_offset_int)

    return time_delta, sign


def get_time_offset(time_zone_abbr):
    time_delta = timedelta(hours=0)
    sign = 0

    if time_zone_abbr in time_offset_dict:
        time_offset = time_offset_dict[time_zone_abbr]
        time_delta, sign = parse_time_offset(time_offset)

    return time_delta, sign


def convert_timestamp_int_list_to_readable_time(timestamp_int_list, time_zone):
    time_delta, sign = get_time_offset(time_zone)
    if time_zone == "unknownTZ" or sign == 0:
        readable_time_str = ["unknown time zone"] * len(timestamp_int_list)
    else:
        timestamp_naive_list = pd.to_datetime(timestamp_int_list, unit='ms', errors='coerce')
        timestamp_TZaware_list = timestamp_naive_list + sign * time_delta
        converter = lambda x: x.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] if pd.notnull(x) else ''
        readable_time_str = pd.Series(map(converter, timestamp_TZaware_list))
        readable_time_str += " " + time_zone

    return readable_time_str


def get_auc_matrix_minute(df_auc_day):
    if df_auc_day.shape[0] == 0:
        return None

    # transform df_mims_day
    ymd_list = []
    hour_list = []
    minute_list = []
    tz_list = []


    for time_str in df_auc_day[0]:
        time_str_components = time_str.split(" ")
        ymd_list.append("-".join([time_str_components[5], time_str_components[1], time_str_components[2]]))
        tz_list.append(time_str_components[4])

    # skip for days with multiple timezone
    tz_set = set(tz_list)
    tz_set_clean = set([x.split("_")[0] for x in tz_set])
    tz_num = len(tz_set_clean)

    datetime_list = convert_timestamp_int_list_to_readable_time(df_auc_day[2], list(tz_set_clean)[0])
    print(datetime_list)
    for ts in datetime_list:
        time_str_components = ts.split(" ")[1].split(":")
        hour_list.append(int(time_str_components[0]))
        minute_list.append(int(time_str_components[1]))

    # iterate through all minutes in a day and find matched time in df_mims_day
    idx = 0
    idx_max = df_auc_day.shape[0]
    hour_min_dict = dict()
    for hour in range(24):
        for min in range(60):
            hour_min = str(hour) + "_" + str(min)

            # temporary measure for days with multiple timezones
            if tz_num > 1:
                hour_min_dict[hour_min] = {"SAMPLE_COUNT": NAN, "AUC_X": NAN, "AUC_Y": NAN, "AUC_Z": NAN}
                continue

            if idx < idx_max:
                hour_min_in_df = str(hour_list[idx]) + "_" + str(minute_list[idx])

            flag = 0
            while hour_min == hour_min_in_df:
                flag = 1

                if hour_min in hour_min_dict:
                    hour_min_dict[hour_min]["SAMPLE_COUNT"] += df_auc_day[3][idx]
                    hour_min_dict[hour_min]["AUC_X"] += df_auc_day[4][idx]
                    hour_min_dict[hour_min]["AUC_Y"] += df_auc_day[5][idx]
                    hour_min_dict[hour_min]["AUC_Z"] += df_auc_day[6][idx]
                else:
                    hour_min_dict[hour_min] = {"SAMPLE_COUNT": df_auc_day[3][idx], "AUC_X": df_auc_day[4][idx], "AUC_Y": df_auc_day[5][idx], "AUC_Z": df_auc_day[6][idx]}

                idx += 1
                if idx == idx_max:
                    break
                hour_min_in_df = str(hour_list[idx]) + "_" + str(minute_list[idx])

            if flag == 0:
                hour_min_dict[hour_min] = {"SAMPLE_COUNT": 0, "AUC_X": NAN, "AUC_Y": NAN, "AUC_Z": NAN}

    YMD = list(set(ymd_list))[0]
    tz = list(tz_set_clean)[0]
    rows = []
    for hour_min in hour_min_dict:
        row = [YMD, hour_min.split("_")[0], hour_min.split("_")[1], tz, hour_min_dict[hour_min]["SAMPLE_COUNT"],
               hour_min_dict[hour_min]["AUC_X"], hour_min_dict[hour_min]["AUC_Y"], hour_min_dict[hour_min]["AUC_Z"]]
        rows.append(row)

    df_minute = pd.DataFrame(rows, columns=colnames)

    return df_minute


if __name__ == "__main__":
    df_mims_day = pd.read_csv(
        r"D:\data\TIME\raw\logs-watch\2021-08-26\06-EDT\Watch-AccelSampling.log.csv", header=None)
    # print(df_mims_day)
    df_minute = get_auc_matrix_minute(df_mims_day)
    df_minute.to_csv(r"C:\Users\Jixin\Downloads\auc_minute.csv")
    print(df_minute[df_minute.HOUR == "6"])
