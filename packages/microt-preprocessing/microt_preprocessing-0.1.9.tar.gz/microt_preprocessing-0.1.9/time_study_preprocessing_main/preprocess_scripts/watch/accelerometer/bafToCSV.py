import gzip
import os
import shutil
import subprocess
from os import sep, getcwd

JAR = getcwd() + sep + "preprocess_scripts" + sep + "utils" + sep + "binarytocsv.jar"


def bafToCsv(file):
    tmpDir = os.path.dirname(file)
    tmpFi = os.path.basename(file)
    tmpFii = tmpFi.replace("AndroidWearWatch-AccelerationCalibrated-NA.", "")
    tmpFull = os.path.join(tmpDir, tmpFii)

    outfilePath = tmpFull[:-4] + '.csv.gz'

    if os.path.exists(outfilePath):
        print(outfilePath + " exists. Skipping binary to csv conversion for this file.")
        return outfilePath
    outPath = os.path.dirname(file)
    try:
        subprocess.call(['java', '-jar', JAR, file, outPath])
    except:
        print('Issue with converting baf file to csv - ' + file)
        return None

    try:
        with open(outfilePath[:-3], 'rb') as f_in:
            with gzip.open(outfilePath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except:
        print('Issue compressing the csv file - ' + outfilePath[:-3])
        return None

    return outfilePath

if __name__ == "__main__":
    file = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\data-watch\2020-06-08\10-EDT\AndroidWearWatch-AccelerationCalibrated-NA.020000000000-AccelerationCalibrated.2020-06-08-10-19-57-375-M0400.sensor.baf"
    # outfilePath = r"C:\Users\jixin\Desktop\temp"
    bafToCsv(file)
