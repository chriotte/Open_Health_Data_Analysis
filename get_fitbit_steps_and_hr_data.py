#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 23:47:26 2017

@author: christopher.ottesen
"""




import pandas as pd 
import fitbit_read as init
from datetime import date, timedelta
from datetime import datetime
import glob, os
import ast
import json

authd_client = init.authd_client
file_path_hr_readings = 'data/fitbit_heart_rate/'

def get_heart_rate(timestamp = "today"):
    heartRates = authd_client.intraday_time_series("activities/heart", base_date=timestamp, detail_level='1sec', start_time=None, end_time=None)
    heartRates = heartRates["activities-heart-intraday"]["dataset"]
    heartRates = pd.DataFrame(heartRates)
    return heartRates

def get_steps(timestamp = "today"):
    steps = authd_client.intraday_time_series("activities/steps", base_date=timestamp, detail_level='1min')
    steps = steps["activities-steps-intraday"]["dataset"]
    steps = pd.DataFrame(steps)
    return steps

def get_sleep(timestamp = "today"):
    sleep = authd_client.sleep(date=timestamp)
    print(sleep)
    sleep = pd.DataFrame(sleep['sleep'])
    return sleep

def steps_to_csv(df,name):
    df.to_csv(file_path_hr_readings+name+".csv", index=False)


def make_Date_list(base_date = "2017-07-12"):
     # the day I got the fitbit
    today = datetime.now().strftime('%Y-%m-%d')
    d1 = date(*map(int, base_date.split("-")))  # start date
    d2 = date(*map(int, today.split("-")))  # end date

    d1 = (d1 + timedelta(days=-1)) # re getting the latest day in case we fetched before the day had ended
    
    delta = d2 - d1         # timedelta
    
    date_range = []
    for i in range(delta.days + 1):
        t = (d1 + timedelta(days=i)).strftime('%Y-%m-%d')
        date_range.append(t)
    return date_range

def find_newest_date():
    allFiles = glob.glob(file_path_hr_readings + "/*.csv")
    date_list = []
    for cur_date in allFiles:
        print(cur_date)
        try:
            cur_date = cur_date.split("/")[2].split(".c")[0]
        except Exception as e:
            print(e)
            cur_date = cur_date.split("\\")[1].split(".c")[0]
            print(cur_date)
        cur_date = date(*map(int, cur_date.split("-")))  # start date
        date_list.append(cur_date)
    return max(date_list) # returns the newst date in the lis

def get_date_range():
    try:
        start_date_from_newest = (find_newest_date()+timedelta(days=1)).strftime('%Y-%m-%d') # we need to add one day to not duplicate
    except:
        start_date_from_newest = "2017-07-12"
    return make_Date_list(start_date_from_newest),start_date_from_newest



from time import sleep
def get_fitbit_data(date_range, func_type = "steps"):
    if func_type == "steps":
        getter = get_steps
    if func_type == "heart":
        getter = get_heart_rate
    if func_type == 'sleep':
        getter = get_sleep

    
    for cur_date in date_range:
        print("Getting date " + cur_date)
        try:
            temp_df = getter(str(cur_date))
            temp_df["date"] = str(cur_date)
            steps_to_csv(temp_df,str(cur_date))
        except Exception as e:
           print("Failed getting data for " + cur_date )
           print(e)
        print("sleeping for a few seconds")
        sleep(5)

def import_fitbit_hr(file_path_hr_readings):
    allFiles = glob.glob(file_path_hr_readings + "/*.csv")
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0)
        list_.append(df)
    return list_

def join_all_csv(file_path='data/fitbit_heart_rate/'):
    all_files = glob.glob(os.path.join(file_path, "*.csv"))

    df_from_each_file = (pd.read_csv(f) for f in all_files)
    return pd.concat(df_from_each_file, ignore_index=True)

def fix_fitbit_sleep():
    concatenated_sleep = join_all_csv(file_path='data/fitbit_sleep/')
    concatenated_df_hour = concatenated_sleep['minuteData']
    concatenated_df_hour = concatenated_df_hour.apply(ast.literal_eval).values.tolist()
    concatenated_df_hour = pd.DataFrame(concatenated_df_hour)
    concatenated_df_hour.index = concatenated_sleep['date']

    concatenated_df_hour = concatenated_df_hour.stack()
    concatenated_df_hour = pd.DataFrame(concatenated_df_hour.values.tolist(), index=concatenated_df_hour.index)
    concatenated_df_hour.reset_index(inplace=True)
    concatenated_df_hour = concatenated_df_hour.rename( columns={"dateTime": "time"})
    concatenated_df_hour.drop('level_1',axis=1).to_csv('data/fitbit_sleep_fixed_file/fitbit_sleep_merged.csv')
    return concatenated_df_hour
# =============================================================================
# Get Newest Fitbit data
# =============================================================================

#Heart rate 
file_path_hr_readings = 'data/fitbit_heart_rate/'
date_range,start_date_from_newest = get_date_range()
print("Reading data from " + start_date_from_newest)
get_fitbit_data(date_range,"heart")

#hr_readings = import_fitbit_hr(file_path_hr_readings)

# Steps data
file_path_hr_readings = 'data/fitbit_steps/'
date_range,start_date_from_newest = get_date_range()
print("Reading data from " + start_date_from_newest)
get_fitbit_data(date_range, "steps")

# sleep data
file_path_hr_readings = 'data/fitbit_sleep/'
date_range,start_date_from_newest = get_date_range()
print("Reading data from " + start_date_from_newest)
get_fitbit_data(date_range, "sleep")



def concatenate_csv_files(file_path='data/fitbit_heart_rate/',value_name = 'heart_rate'):
    concatenated_df = join_all_csv(file_path=file_path)
    concatenated_df['timestamp'] = concatenated_df['date'] + ' ' + concatenated_df['time']
    concatenated_df = concatenated_df[['timestamp','value']]
    concatenated_df = concatenated_df.rename(index=str, columns={"value": value_name})
    return concatenated_df

concatenated_hr = concatenate_csv_files(file_path='data/fitbit_heart_rate/',value_name = 'heart_rate')
concatenated_steps = concatenate_csv_files(file_path='data/fitbit_steps/',value_name = 'steps')

fix_fitbit_sleep()
concatenated_sleep = concatenate_csv_files(file_path='data/fitbit_sleep_fixed_file/',value_name = 'sleep_stage')

def merge_dataframes(df1,df2):
    merged = pd.merge(df1, df2,how='outer', on='timestamp')
    return merged

def merged_to_datetime(merged):
    merged['timestamp'] = pd.to_datetime(merged['timestamp'], format='%Y-%m-%d %H:%M:%S')
    merged = merged.sort_values(by='timestamp')
    return merged

merged = merge_dataframes(concatenated_hr,concatenated_steps)
merged = merge_dataframes(merged,concatenated_sleep)
merged = merged_to_datetime(merged)

merged['steps'] =merged['steps'].fillna(0)
merged['heart_rate']= merged['heart_rate'].fillna(merged['heart_rate'].rolling(min_periods=1, center=True, window=12).median())
merged['sleep_stage']= merged['sleep_stage'].fillna(merged['sleep_stage'].rolling(min_periods=1, center=True, window=12).median())
merged['sleep_stage']= merged['sleep_stage'].fillna(merged['sleep_stage'].rolling(min_periods=1, center=True, window=2).median())
merged['sleep_stage'] = merged['sleep_stage'].fillna(0) # for being awake

# merged['sleep_stage_multiplied'] = merged['sleep_stage']*20


merged.to_csv('merged_hr_sleep_steps.csv',index=False)


merged.plot(x='timestamp',y=['heart_rate','sleep_stage'])

