#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 22:09:08 2017

@author: christopher
"""

import sys
sys.path.append("fitbitlib/")

import keys
import fitbit
import pandas as pd


# add secret keys here 
consumerKey = keys.consumerKey
consumerSecret = keys.consumerSecret
access_token = keys.access_token
refresh_token = keys.refresh_token

authd_client = fitbit.Fitbit(consumerKey, consumerSecret,
                             access_token=access_token, refresh_token=refresh_token)

# reads a dataframe om nutrition data
df = pd.read_csv('data/nutData.csv')


# function to log food
def logFood(foodName = "default",date,calories = 0 ,carbs = 0,fat = 0,fiber = 0,protein = 0,sodium= 0):
    fooddata = {
            'foodName': foodName,
            'mealTypeId':7,
            'unitId': 304,
            'amount': 1,
            'date': date,
            "calories":calories,
            "totalCarbohydrate":carbs,
            "totalFat":fat,
            "dietaryFiber":fiber,
            "protein":protein,
            "sodium":sodium
    
    }
          
    authd_client.foods_log(date=date, user_id=None, data=fooddata)


# reads trough each day in the dataframe and logs the content
for index, row in df.iterrows():
    Date = row['Date']
    Calories = int(row['Calories'])
    Carbohydrates = row['Carbohydrates']
    Fat = row['Fat']
    Fiber = row['Fiber']
    Protein = row['Protein']
    Sodium = row['Sodium (mg)']
    #uncomment to do the posting
    #logFood("Default",Date,Calories,Carbohydrates,Fat,Fiber,Protein,Sodium)
    
    

