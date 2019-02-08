import pandas as pd
import glob
import datetime
import time

start_time = time.time()



def get_json_to_df(file_list = []):
    df_list = []
    for json_file in file_list:
        df_list.append(pd.read_json(json_file))
    df = pd.concat(df_list)
    return df

def merge_dataframes(df1,df2):
    merged = pd.merge(df1, df2,how='outer', on='dateTime')
    return merged

def merged_to_datetime(merged):
    merged['dateTime'] = pd.to_datetime(merged['dateTime'], format='%m/%d/%y %H:%M:%S')
    merged = merged.sort_values(by='dateTime')
    return merged


## Creating lists of all the respective files in the directory
heart_rate_file_list = glob.glob('data/Fitbit_data_export/user-site-export/heart_rate-*')
steps_file_list = glob.glob('data/Fitbit_data_export/user-site-export/steps-*')
altitude_file_list = glob.glob('data/Fitbit_data_export/user-site-export/altitude-*')
calories_file_list = glob.glob('data/Fitbit_data_export/user-site-export/calories-*')


making_file_lists = time.time()
print("###Time taken to make files lists",making_file_lists-start_time)

## reading json into dataframes
heart_rate_df = get_json_to_df(file_list = heart_rate_file_list).reset_index()
## Heart rate contains a sub json that are explicitly converted into column

def make_new_df_value(x='',column_name=''):
    try:
        x = x[column_name]
    except Exception as e:
        print(e)
        x = 0.0
    return x
    

heart_rate_df['bpm'] = heart_rate_df['value'].transform(lambda x: x['bpm'])
heart_rate_df['confidence'] = heart_rate_df['value'].transform(lambda x: x['confidence'])
heart_rate_df = heart_rate_df.drop(['value','index'],axis=1)


steps_df = get_json_to_df(file_list = steps_file_list).rename(columns={'value': 'steps'})

altitude_df = get_json_to_df(file_list = altitude_file_list).rename(columns={'value': 'altitude'})
calories_df = get_json_to_df(file_list = calories_file_list).rename(columns={'value': 'calories'})

load_json_time = time.time()
print("###Time taken to load and transform json files",load_json_time-making_file_lists)


merged = merge_dataframes(heart_rate_df,steps_df)
merged = merge_dataframes(merged,altitude_df)
merged = merge_dataframes(merged,calories_df)
merged = merged_to_datetime(merged)

merged.to_csv('merged_export_data.csv')

merging_time = time.time()
print("###Time taken to merge dataframess",merging_time-load_json_time)



function_time = time.time() - start_time
print('## Time taken',function_time) 