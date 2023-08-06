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
                    'Question_X_ID',
                    'Question_X_Text',
                    'Question_X_Answer_Text ',
                    'Question_X_Answer_Unixtime']

    df_hour_raw.columns = column_names
    return df_hour_raw


if __name__ == "__main__":
    target_file = "PromptResponses.log.csv"
    hour_folder_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT\aditya4_internal@timestudy_com\logs-watch\2020-05-31\10-EDT"
    target_file_path = hour_folder_path + sep + target_file
    output_file_path = r"C:\Users\jixin\Desktop\temp\temp_file.csv"
    p_id = "aditya4_internal@timestudy_com"

    df_hour_raw = pd.read_csv(target_file_path, header=None)
    print(df_hour_raw)
    df_hour_parsed = parse_raw_df(df_hour_raw, p_id)
    df_hour_parsed.to_csv(output_file_path, index=False)
