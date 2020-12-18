#!/usr/bin/env python
# coding: utf-8

# webscraping congregate settings

# Dependencies
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import time

congregate_f = "E:/batch/dashboard_covid19/shelters/content/homeless_service.csv"
# Boilerplate code
url = 'http://publichealth.lacounty.gov/media/Coronavirus/locations.htm'
res = requests.get(url)
html_page = res.content

# ## Parse through the html
soup = BeautifulSoup(html_page, 'html.parser')
#print(soup.prettify())

# Load data to a Pandas dataframe

# column names
column = ['obs', 'setting', 'type', 'staff_case', 'res_case', "deaths "]

# empty list
data = []
count = 0
# Find the third instance of this type of class
table = soup.findAll("table", {"table table-striped table-bordered table-sm overflow-y"})[4]#.findAll('tr')
for element in table.findAll("tr"):
    count += 1
    if count > 1:
        # find cells containing td
        cells = element.findAll("td")
        info = [cell.text for cell in cells] # get the cell text
        data.append(info) # append to data list
        # print(data)
        time.sleep(2)
        
df_cong = pd.DataFrame(data, columns= column,) # convert to dataframe
print(df_cong.head())

df_cong.to_csv(congregate_f, encoding='utf-8', index=False)

df_cong = pd.read_csv(congregate_f, index_col=False)

# Add today's date to the dataframe
import datetime
def today_date():
    '''
    utils:
    get the datetime of today
    '''
    date=datetime.datetime.now().date()
    date=pd.to_datetime(date)
    return date
df_cong['Date_'] = today_date()

# Explicitly convert Date field to date

df_cong['Date_'] = pd.to_datetime(df_cong['Date_']).dt.date


df_cong.to_csv("E:/batch/dashboard_covid19/shelters/content/congregate_day.csv", encoding='utf-8', index=False)

# ## Now let's deal with the existing database
# ### This existing database contains previous days' data

dfDB = pd.read_csv("E:/batch/dashboard_covid19/shelters/content/congregate_storage.csv", parse_dates=['Date_'])#, dayfirst=True)

# ## If current day's date is already in database, delete it
for index, row in dfDB.iterrows():
    #print(row['Date'])
    if row['Date_'] == today_date():
        #print('Found')
        dfDB.drop(index, inplace=True)
    else:
        pass

# ## Then let's add the newly scraped data to the database
df= dfDB.append(df_cong, ignore_index = True,sort=True)
df['Date_'] = pd.to_datetime(df['Date_']).dt.strftime('%m/%d/%Y')


df.head()

# Convert location field to upper
# so it can join with communities shapefile
##df['location'] = df.location.str.upper()
# handle empty cells, they are not read as NaN by default
#df['rate'].replace('', np.nan, inplace=True)
# now they can be deleted
#df.dropna(subset=['rate'], inplace=True)
df.to_csv("E:/batch/dashboard_covid19/shelters/content/congregate_storage.csv", encoding='utf-8', index=False)
print(df.head())
