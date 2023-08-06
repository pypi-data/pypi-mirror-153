import os
from os import path, sep, getcwd
import importlib
import time
import shutil

import time_study_preprocessing_main.preprocess_scripts


# participant_text_file_path = getcwd() + sep + "analysis_task" + sep + device + "_participants_included.txt"

def preprocessing_start(microT_root_path, intermediate_file_save_path, delete_raw, date):
    device = 'watch'
    module_name = '.main'
    information_text_file_path = getcwd() + sep + "analysis_task" + sep + device + "_information_included.txt"
    information_list = ["prompt_response", "battery_level", "watch_accel_sampling", "dnd_status", "power_status",
                        "uema_undo_counts", "accelerometer"]
    # information_list = ["battery_level"]
    # parse information and participants text file
    # information_list = preprocess_scripts.utils.parse_information.parse_information(information_text_file_path)
    # p_id_list = []
    # if participant_text_file_path.endswith('.txt'):
    #     p_id_list = preprocess_scripts.utils.parse_participants.parse_participants(participant_text_file_path)
    # else:
    #     p_id_with_domain = participant_text_file_path + '@timestudy_com'
    #     p_id_list.append(p_id_with_domain)
    t0 = time.time()
    # for p_id in p_id_list:
    #     print("Watch pre-processing for: " + str(p_id))
    #     p_id_logs = microT_root_path + sep + p_id + sep + 'logs-watch'
    #     p_id_data = microT_root_path + sep + p_id + sep + 'data-watch'
    p_id_logs = microT_root_path + sep + 'logs-watch'
    p_id_data = microT_root_path + sep + 'data-watch'
    root_path_components = microT_root_path.split(sep)
    p_id = root_path_components[len(root_path_components) - 1]
    if path.exists(p_id_logs):
        # date_list = preprocess_scripts.utils.validate_dates.get_relevant_date_list(p_id_logs, date_start, date_end)
        # for date in date_list:
        # iterate through info
        for info in information_list:
            module_path = "time_study_preprocessing_main.preprocess_scripts." + device + '.' + info
            preprocess_module = importlib.import_module(module_name, module_path)
            # pre-process
            preprocess_module.pre_process(microT_root_path, intermediate_file_save_path, p_id, date)
        if delete_raw == "1":
            p_id_logs_date = p_id_logs + sep + date
            p_id_data_date = p_id_data + sep + date
            if path.exists(p_id_logs_date):
                print("Deleting: " + str(p_id_logs_date))
                shutil.rmtree(p_id_logs_date)
            # if path.exists(p_id_data_date):
            #     shutil.rmtree(p_id_data_date)
    # if delete_raw == "1":
    #     if len(os.listdir(p_id_logs)) == 0:
    #         shutil.rmtree(p_id_logs)
    #     if len(os.listdir(p_id_data)) == 0:
    #         shutil.rmtree(p_id_data)

    t1 = time.time()
    print("Time elapsed is  {} secs : \n".format((t1 - t0)))


def run_uema_main(microT_root_path, intermediate_file_save_path, delete_raw, date_start):
    # try: argv = sys.argv[1:] microT_root_path, intermediate_file_save_path, participant_text_file_path, delete_raw,
    # date_start, date_end, hourKeep = \ preprocess_scripts.utils.parse_cml_argv.parse_arguments_uema( argv) except:
    # preprocess_scripts.utils.parse_cml_argv.printHelpOptions() sys.exit( 'Errors : Incorrect Command Line
    # Arguments. Please correct your arguments according to the references ' 'above.')

    # pre processing
    preprocessing_start(microT_root_path, intermediate_file_save_path, delete_raw, date_start)

# if __name__ == "__main__":
#     # parse arguments try: argv = sys.argv[1:] microT_root_path, intermediate_file_save_path,
#     # participant_text_file_path, delete_raw, date_start, date_end, hourKeep = \
#     # preprocess_scripts.utils.parse_cml_argv.parse_arguments_uema( argv) except:
#     # preprocess_scripts.utils.parse_cml_argv.printHelpOptions() sys.exit( 'Errors : Incorrect Command Line
#     # Arguments. Please correct your arguments according to the references ' 'above.')
#     #
#     # # pre processing
#     # preprocessing_start(microT_root_path, intermediate_file_save_path, participant_text_file_path,
#     #                     delete_raw, date_start, date_end)
#     time_study_preprocessing_main()
