#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 16:07:20 2017

@author: christopher
"""

import pandas as pd
from pandas import DataFrame
import glob
import datetime
import re


def createTimestamps(df,time):    
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H-%M-%S')

    firstTime = time + datetime.timedelta(milliseconds=0) 
    curTime = time
    lastTime = time
    df["time"] = firstTime
    for i, row in df.iterrows():
        if i == 0:
            curTime = time
            lastTime = curTime
            df.loc[i, 'time'] = time + datetime.timedelta(milliseconds=0)
        else:

            curTime = lastTime + datetime.timedelta(milliseconds=row["interval in seconds"])
            df.loc[i, 'time']  = curTime
            lastTime = curTime

    return df


def importDriveData(file,type):
    print("Reading files")
    df = DataFrame()

    allFiles = glob.glob(path + type)
    allFiles.sort()
   # print(allFiles)
    count = 0
    for file in allFiles:
        time = ((re.sub(r'.*/20', '20', file)).rsplit('.txt', 1))[0]
        print(time)
        
        
        print("File: ", file)
        if (count == 0): # first run
             df = pd.read_table(file, skiprows=None, header=None, delim_whitespace=True)
             df.columns = ["interval in seconds"]
            # print("Create timestamps")
             df = createTimestamps(df,time)
             
        else:
             dftemp = pd.read_table(file, skiprows=None, header=None, delim_whitespace=True)
             dftemp.columns = ["interval in seconds"]
             dftemp= createTimestamps(dftemp,time)
             df = df.append(dftemp)
             
        count+=1
    

    return df


path = 'data/eliteHRV/export/'

elite = importDriveData(path, "*.txt")

elite.reset_index().plot(x="time", y=['interval in seconds'])

