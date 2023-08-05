import gzip
import os
import shutil
import subprocess
from os import sep, getcwd
from io import StringIO
import pandas as pd
import datetime
import struct
import warnings

warnings.filterwarnings("ignore")

JAR = getcwd() + sep + "preprocess_scripts" + sep + "utils" + sep + "readBinaryFile.jar"
G_VAL = 9.80

# col = ["Check", "HEADER_TIME_STAMP", "X_ACCELERATION_METERS_PER_SECOND_SQUARED",
#        "Y_ACCELERATION_METERS_PER_SECOND_SQUARED", "Z_ACCELERATION_METERS_PER_SECOND_SQUARED"]

col = ["HEADER_TIME_STAMP", "X_ACCELERATION_METERS_PER_SECOND_SQUARED",
       "Y_ACCELERATION_METERS_PER_SECOND_SQUARED", "Z_ACCELERATION_METERS_PER_SECOND_SQUARED"]


# def baf_to_dataframe(file):
#     print('inside binary to df')
#     print(str(file))
#     tmpDir = os.path.dirname(file)
#     tmpFi = os.path.basename(file)
#     tmpFii = tmpFi.replace("AndroidWearWatch-AccelerationCalibrated-NA.", "")
#     tmpFull = os.path.join(tmpDir, tmpFii)
#
#     tz = os.path.basename(tmpFull).split('-')[-1].split('.')[0]
#     if not tz.startswith('M') and not tz.startswith('P'):
#         print("The last argument in the filename before 'sensor' should contain timeoffset term starting with M or p")
#         return
#
#     try:
#         a = subprocess.Popen(['java', '-jar', JAR, file], stdout=subprocess.PIPE)
#     except:
#         print('Issue with converting baf file to csv - ' + str(tmpFull))
#         return None
#
#     b = StringIO(a.communicate()[0].decode('utf-8'))
#
#     df = pd.read_csv(b, sep=",", names=col)
#     df = df.loc[df['Check'] == "Relevant data"]
#     df.drop(columns=['Check'], inplace=True)
#     return df

def baf_to_dataframe(file):
    tz = os.path.basename(file).split('.')[2].split('-')[-1]

    hourdiff = int(tz[1:3])
    minutediff = int(tz[3:])

    if tz[0] == 'M':
        hourdiff = -int(tz[1:3])
        minutediff = -int(tz[3:])

    in_file = open(file, "rb")
    b = in_file.read(20)
    diction = {}
    i = 0
    while len(b) >= 20:
        t = int.from_bytes(b[0:8], byteorder='big')
        x = struct.unpack('>f', b[8:12])[0]
        y = struct.unpack('>f', b[12:16])[0]
        z = struct.unpack('>f', b[16:20])[0]
        diction[i] = {'time': t, 'x': x, 'y': y, 'z': z}
        i = i + 1

        b = in_file.read(20)

    df = pd.DataFrame.from_dict(diction, "index")
    df.columns = col
    df['HEADER_TIME_STAMP'] = pd.to_datetime(df['HEADER_TIME_STAMP'], unit='ms') + \
                              datetime.timedelta(hours=hourdiff) + datetime.timedelta(minutes=minutediff)
    df['X_ACCELERATION_METERS_PER_SECOND_SQUARED'] = df['X_ACCELERATION_METERS_PER_SECOND_SQUARED']/G_VAL
    df['Y_ACCELERATION_METERS_PER_SECOND_SQUARED'] = df['Y_ACCELERATION_METERS_PER_SECOND_SQUARED']/G_VAL
    df['Z_ACCELERATION_METERS_PER_SECOND_SQUARED'] = df['Z_ACCELERATION_METERS_PER_SECOND_SQUARED']/G_VAL
    return df


if __name__ == "__main__":
    file = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\data-watch" \
           r"\2020-06-08\10-EDT\AndroidWearWatch-AccelerationCalibrated-NA.020000000000-AccelerationCalibrated.2020" \
           r"-06-08-10-19-57-375-M0400.sensor.baf "
    # outfilePath = r"C:\Users\jixin\Desktop\temp"
    baf_to_dataframe(file)
