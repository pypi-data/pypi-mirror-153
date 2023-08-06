from os import sep
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def parse_raw_df(df_hour_raw, p_id):
    column_names = ['Participant_ID', 'Prompt_Type', 'Study_Mode', 'Prompt_Trigger', 'Time_Window_Start',
                    'Time_Window_End', 'Initial_Prompt_Date', 'Initial_Prompt_Local_Time', 'Initial_Prompt_UTC_Offset ',
                    'Initial_Prompt_UnixTime',
                    'Answer_Status',
                    'Reprompt1_Prompt_Date',
                    'Reprompt1_Prompt_Local_Time',
                    'Reprompt1_Prompt_UnixTime',
                    'Reprompt2_Prompt_Date',
                    'Reprompt2_Prompt_Local_Time',
                    'Reprompt2_Prompt_UnixTime ',
                    'Reprompt3_Prompt_Date',
                    'Reprompt3_Prompt_Local_Time',
                    'Reprompt3_Prompt_UnixTime',
                    'Reprompt4_Prompt_Date',
                    'Reprompt4_Prompt_Local_Time',
                    'Reprompt4_Prompt_UnixTime',
                    'Reprompt5_Prompt_Date',
                    'Reprompt5_Prompt_Local_Time',
                    'Reprompt5_Prompt_UnixTime',
                    'Question_Set_Completion_Date',
                    'Question_Set_Completion_Local_Time',
                    'Question_Set_Completion_UnixTime',
                    'Question_Set_Completion_Prompt_Number',
                    'Probabilistic_Question_Set_Selected',
                    'Number_Of_Questions_Presented',
                    'Survey version number',
                    'Question_1_ID'
                    # 'Question_X_Text',
                    # 'Question_X_Answer_Text ',
                    # 'Question_X_Answer_Unixtime'
                    ]
    # name the first 33 columns
    column_indices = range(len(column_names))
    new_names = column_names
    old_names = df_hour_raw.columns[column_indices]
    df_hour_raw.rename(columns=dict(zip(old_names, new_names)), inplace=True)

    # name the rest of the columns
    column_indices_questions = range(33, df_hour_raw.shape[1])
    new_names = []
    for qNum in range(1, int((df_hour_raw.shape[1] - 33) / 4) + 1):
        new_name_per_question = [x.replace("X", str(qNum)) for x in
                                 ['Question_X_ID', 'Question_X_Text', 'Question_X_Answer_Text ',
                                  'Question_X_Answer_Unixtime']]
        new_names += new_name_per_question
    old_names = df_hour_raw.columns[column_indices_questions]
    df_hour_raw.rename(columns=dict(zip(old_names, new_names)), inplace=True)

    return df_hour_raw


if __name__ == "__main__":
    target_file = "PromptResponses.log.csv"
    hour_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\stephen2_internal@timestudy_com\logs\2020-05-06\21-EDT"
    target_file_path = hour_folder_path + sep + target_file
    output_file_path = r"C:\Users\jixin\Desktop\temp\temp_file.csv"
    p_id = "stephen2_internal@timestudy_com"

    df_hour_raw = pd.read_csv(target_file_path, header=None)
    # print(df_hour_raw)
    df_hour_parsed = parse_raw_df(df_hour_raw, p_id)
    df_hour_parsed.to_csv(output_file_path, index=False)
