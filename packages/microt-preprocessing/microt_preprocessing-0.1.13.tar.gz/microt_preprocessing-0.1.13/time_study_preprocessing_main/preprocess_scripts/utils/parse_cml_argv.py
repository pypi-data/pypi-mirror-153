import os
import re
import sys

help_text = '''
--------------------------:
Command line help options |
--------------------------:
    * Make sure your current working directory is the root of project folder.

    Usage:
        python preprocessing_all_ema.py <microT_root_path> <intermediate_file_save_path> <participants_included_text_file_path> [date_start] [date_end] <-o>
        python preprocessing_all_ema.py <microT_root_path> <intermediate_file_save_path> <participants_included_text_file_path> [date_start] [date_end]
        python preprocessing_all_ema.py <microT_root_path> <intermediate_file_save_path> <participants_included_text_file_path> [date_start] 
        python preprocessing_all_ema.py <microT_root_path> <intermediate_file_save_path> <participants_included_text_file_path> 
        python preprocessing_all_ema.py [-h]

    Options:
        -o, --hour          Keep hourly file temporarily generated during the pre-process
        -h, --help          Display command line help options
'''


def printHelpOptions():
    print(help_text)


def isPath(path_str):
    isDirectory = os.path.isdir(path_str)
    isFile = os.path.isfile(path_str)
    isPath = isDirectory or isFile
    return isPath


def parse_arguments_ema(argv):
    # usage : python preprocessing_all_ema.py [-h]
    for arg in argv:
        if arg == "-h" or arg == "--help":
            raise SystemExit()

    # check the first four positional arguments
    if len(argv) >= 4:
        allPaths = True
        for i in range(0, 2):
            # allPaths = allPaths and isPath(argv[i])
            allPaths = True
        if allPaths:
            microT_root_path = argv[0]
            intermediate_file_save_path = argv[1]
            # participant_text_file_path = argv[2]
            decrypt_password = argv[2]
            delete_raw = argv[3]
        else:
            print("Error : The first three arguments should be valid paths")
            raise SystemExit()
    else:
        print("Error : Fewer arguments than expected")
        raise SystemExit()

    # usage: with three or more positional arguments
    date_args = [x for x in argv if bool(re.match(r'(\d+\-\d+)', x))]
    # usage : with no date arguments
    if len(date_args) == 0:
        print("Must pass a date argument. Exiting ...")
        sys.exit(1)
    elif len(date_args) == 1:
        date_start = argv[4]
        # date_end = date_start
    elif len(date_args) == 2:
        date_start = argv[4]
        # date_end = date_start
    else:
        print("Error : Wrong number of date arguments")
        raise SystemExit()

    # find if user wants to keep hourly file
    # hourKeep = False
    # for arg in argv:
    #     if arg == "-o" or arg == "--hour":
    #         hourKeep = True

    return microT_root_path, intermediate_file_save_path, decrypt_password, delete_raw, date_start


def parse_arguments_uema(argv):
    # usage : python preprocessing_all_ema.py [-h]
    for arg in argv:
        if arg == "-h" or arg == "--help":
            raise SystemExit()

    # check the first four positional arguments
    if len(argv) >= 4:
        allPaths = True
        for i in range(0, 2):
            allPaths = allPaths and isPath(argv[i])
        if allPaths:
            microT_root_path = argv[0]
            intermediate_file_save_path = argv[1]
            participant_text_file_path = argv[2]
            # decrypt_password = argv[3]
            delete_raw = argv[3]
        else:
            print("Error : The first three arguments should be valid paths")
            raise SystemExit()
    else:
        print("Error : Fewer arguments than expected")
        raise SystemExit()

    # usage: with three or more positional arguments
    date_args = [x for x in argv if bool(re.match(r'(\d+\-\d+)', x))]
    # usage : with no date arguments
    if len(date_args) == 0:
        print("Must pass a date argument. Exiting ...")
        sys.exit(1)
    elif len(date_args) == 1:
        date_start = argv[4]
        # date_end = date_start
    elif len(date_args) == 2:
        date_start = argv[4]
        # date_end = argv[5]
    else:
        print("Error : Wrong number of date arguments")
        raise SystemExit()

    # find if user wants to keep hourly file
    # hourKeep = False
    # for arg in argv:
    #     if arg == "-o" or arg == "--hour":
    #         hourKeep = True

    return microT_root_path, intermediate_file_save_path, participant_text_file_path, delete_raw, date_start


if __name__ == "__main__":
    argv = sys.argv[1:]
    parse_arguments_uema(argv)
    parse_arguments_ema(argv)
