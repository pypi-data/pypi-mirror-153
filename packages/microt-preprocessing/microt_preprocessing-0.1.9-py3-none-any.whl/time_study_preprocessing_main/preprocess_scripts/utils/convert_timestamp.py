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


if __name__ == "__main__":
    sample_csv_path = r"E:\intermediate_file\aditya4_internal@timestudy_com\2020-06-03\phone_app_usage_clean_hour_temp\phone_app_usage_clean_03-EDT.csv"
    time_zone = "EDT"
    df = pd.read_csv(sample_csv_path)
    print(convert_timestamp_int_list_to_readable_time(df['LAST_HOUR_TIMESTAMP'], time_zone))
    # print("{} is translated to {} .".format(str(timestamp_int), convert_timestamp2string(timestamp_int, time_zone)))
