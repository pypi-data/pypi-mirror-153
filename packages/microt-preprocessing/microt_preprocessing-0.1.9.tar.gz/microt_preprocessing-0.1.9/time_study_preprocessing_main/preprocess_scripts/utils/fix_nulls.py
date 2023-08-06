def fix_nulls(s):
    for line in s:
        yield line.replace('\0', '')


if __name__ == "__main__":
    area_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\logs-watch"
    date_start = "2020-01-01"
    date_end = "2020-07-01"

    fixed_string = fix_nulls(area_folder_path)
