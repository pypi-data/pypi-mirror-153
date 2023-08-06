from os import sep
import pandas as pd
import numpy as np
import warnings

# warnings.filterwarnings("ignore")
NAN = np.nan
colnames = ["YEAR_MONTH_DAY", "HOUR", "MINUTE", "TIMEZONE", "MIMS_SAMPLE_NUM", "MIMS_INVALID_SAMPLE_NUM", "MIMS_SUM"]


def get_mims_matrix_minute(df_mims_day):
    if df_mims_day.shape[0] == 0:
        return None

    # transform df_mims_day
    ymd_list = []
    hour_list = []
    minute_list = []
    tz_list = []
    for time_str in df_mims_day["HEADER_TIME_STAMP"]:
        hour_min_millisecond = time_str.split(" ")[1]
        hour_min_second = hour_min_millisecond.split(".")[0]
        hour_min_second_components = hour_min_second.split(":")

        hour_list.append(int(hour_min_second_components[0]))
        minute_list.append(int(hour_min_second_components[1]))
        ymd_list.append(time_str.split(" ")[0])
        tz_list.append(time_str.split(" ")[2])

    # skip for days with multiple timezone
    tz_set = set(tz_list)
    tz_set_clean = set([x.split("_")[0] for x in tz_set])
    tz_num = len(tz_set_clean)

    # iterate through all minutes in a day and find matched time in df_mims_day
    idx = 0
    idx_max = df_mims_day.shape[0]
    hour_min_dict = dict()
    for hour in range(24):
        for min in range(60):
            hour_min = str(hour) + "_" + str(min)

            # temporary measure for days with multiple timezones
            if tz_num > 1:
                hour_min_dict[hour_min] = {"MIMS_SAMPLE_NUM": NAN, "MIMS_INVALID_SAMPLE_NUM": NAN, "MIMS_SUM": NAN}
                continue

            if idx < idx_max:
                hour_min_in_df = str(hour_list[idx]) + "_" + str(minute_list[idx])

            flag = 0
            while hour_min == hour_min_in_df:
                flag = 1

                mims_value_sec = df_mims_day["MIMS_UNIT"][idx]
                invalid_sample_num = 0
                if mims_value_sec < 0:  # convert -0.01 to 0
                    mims_value_sec = 0
                    invalid_sample_num = 1

                if hour_min in hour_min_dict:
                    hour_min_dict[hour_min]["MIMS_SAMPLE_NUM"] += 1
                    hour_min_dict[hour_min]["MIMS_SUM"] += mims_value_sec
                    hour_min_dict[hour_min]["MIMS_INVALID_SAMPLE_NUM"] += invalid_sample_num
                else:
                    hour_min_dict[hour_min] = {"MIMS_SAMPLE_NUM": 1, "MIMS_INVALID_SAMPLE_NUM": invalid_sample_num,
                                               "MIMS_SUM": mims_value_sec}

                idx += 1
                if idx == idx_max:
                    break
                hour_min_in_df = str(hour_list[idx]) + "_" + str(minute_list[idx])

            if flag == 0:
                hour_min_dict[hour_min] = {"MIMS_SAMPLE_NUM": 0, "MIMS_INVALID_SAMPLE_NUM": NAN, "MIMS_SUM": NAN}

    YMD = list(set(ymd_list))[0]
    tz = list(tz_set_clean)[0]
    rows = []
    for hour_min in hour_min_dict:
        row = [YMD, hour_min.split("_")[0], hour_min.split("_")[1], tz, hour_min_dict[hour_min]["MIMS_SAMPLE_NUM"],
               hour_min_dict[hour_min]["MIMS_INVALID_SAMPLE_NUM"], hour_min_dict[hour_min]["MIMS_SUM"]]
        rows.append(row)

    df_minute = pd.DataFrame(rows, columns=colnames)

    return df_minute


if __name__ == "__main__":
    df_mims_day = pd.read_csv(
        r"D:\data\TIME\intermediate_sample\idealistsustainerexpansive@timestudy_com\2021-11-07\watch_accelerometer_mims_clean_2021-11-07.csv")
    df_minute = get_mims_matrix_minute(df_mims_day)
    print(df_minute)
