# Open Health Data Analysis 
 
Devices such as Fitbit et al can measure the body 24/7, but unfortunately, it can be difficult to extract and access this data. The goal of this repository is to have a set of scripts that fetches the full datasets and then does some clever analysis of the data. 

## Collaboraters needed
This project started out as a simple script that has gradually been extended, collaborators are very welcome to clean up scripts, extend them, as well as add scripts for more devices and data sources. 

### Current state of the project: 
#### Fitbit
1. get_fitbit_steps_and_hr_data.py 
Gathers minute by minute steps, heart rate, and sleep data, and does a simple exploratory data analysis. 
Much more potential here, both in terms of getting more data and doing a more clever analysis. 

2. fitbitWrite.py
Contains a script to write nutrition data from other sources such as myfitnesspal to Fitbit. This script was originally created to sync my data between the two sources. 

3. fitbit_read.py
Handles connections to the Fitbit API, through the [Python Fitbit](https://github.com/orcasgit/python-fitbit) project.

#### Other
1. readAppleHealth.py
Converts data from Apple Health to a pandas dataframe. Based on this [Github Repository](https://gist.github.com/thomaswilley/5079f1106b1ddf2c71b6)
2. get_yolanda.py
Imports and plots data from exported .csv from Yolanda smart scales
3. EliteHRV
This script has been moved to a [seperate repo](https://github.com/chriotte/EliteHRV_to_dataframe). 
Reads and plots RR intervals from EliteHRV


## Getting Started

UPDATE: use this tutorial to get keys from Fitbit https://towardsdatascience.com/collect-your-own-fitbit-data-with-python-ff145fa10873


### Getting started
To use the FitBit API a file named "keys.py" containing access information must be updated with CLIENT_ID and CLIENT_SECRET.
The keys can be created by making a new app with FitBits API here: https://dev.fitbit.com/ 

Step 1: Set up your account and create the app

The first thing you’ll need to do is create a Fitbit account. Once you’ve done that, you can go to dev.fitbit.com. Under “Manage”, go to “Register An App”.

For the application website and organization website, name it anything starting with “http://” or “https://”. Secondly, make sure the OAuth 2.0 Application Type is “Personal” as this is key to allowing us to download our intraday data. Lastly, make sure the Callback URL is “http://127.0.0.1:8080/” in order to get our Fitbit API to connect properly. After that, click on the agreement box and submit.

Step 2:
Cop the OAuth 2.0 Client ID and the Client Secret into the python script.

#### Fetching Steps, Heart Rate and sleep logs
Note, the script looks for previous files in the data folder and starts fetching new data after the existing date.
If there are no previous files, the start_date_from_newest parameter in fitbit_read.py should be updated to a suitable date (eg the day you first started wearing your Fitbit). 

```
def get_date_range():
    try:
        start_date_from_newest = (find_newest_date()+timedelta(days=1)).strftime('%Y-%m-%d') # we need to add one day to not duplicate
    except:
        start_date_from_newest = "2017-07-12"
    return make_Date_list(start_date_from_newest),start_date_from_newest
```

To start downloading data, the easiest is to run the data_analysis.ipynb Notebook that currently works as an interface to the fetching code. The same code can also be run by running fitbit_read.py, but this file will be reworked into a more tidy class file at a later stage. 

The script will connect to Fitbit and download data until today's date (note, it overwrites the last .csv files as those might be from an incomplete day if it was fetched eg in the middle of the day).
When all the csv are fetched, the script will merge it into one .csv based on timestamps.

### Importing a .csv to FitBit

Import a .csv of nutrition data into FitBit.
Use the function found in the fitbitWrite.py file called logFood() - This file takes the following parameters.
foodName,date,calories,carbs,fat,fiber ,protein,sodium):

Example:
```
logFood("Default",Date,Calories,Carbohydrates,Fat,Fiber,Protein,Sodium)```


```
This can be incorporated into a for loop to post each DataFrame entry to the FitBit API:

```
df = pd.read_csv('data/nutData.csv')


for index, row in df.iterrows():
    Date = row['Date']
    Calories = int(row['Calories'])
    Carbohydrates = row['Carbohydrates']
    Fat = row['Fat']
    Fiber = row['Fiber']
    Protein = row['Protein']
    Sodium = row['Sodium (mg)']
    logFood("Default",Date,Calories,Carbohydrates,Fat,Fiber,Protein,Sodium)
    
    
```


## Authors

* **Christopher Ottesen** 


## Acknowledgments
Thanks to python-fitbit for their hard work!
* https://github.com/orcasgit/python-fitbit

Thanks to Thomas Willey for the code that reads Apple Health Data into a DF
* https://gist.github.com/thomaswilley/5079f1106b1ddf2c71b6