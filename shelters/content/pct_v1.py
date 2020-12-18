#!/usr/bin/env python
# coding: utf-8

# Dependencies
import pandas as pd
import numpy as np
from datetime import datetime


# Set variables
df = pd.read_csv("./content/congregate_storage.csv", encoding='utf-8')#, index=False)
df['Date'] = pd.to_datetime(df['Date_'])
df['day_of_week'] = df['Date'].dt.day_name()

# Create the data frame of the current day of the week
# Very important for the percent change
dval = datetime.today().strftime('%A')
df = df.loc[(df['day_of_week']== dval)] 

# Identify fields to use
new = df[['Date', 'setting','res_case', 'staff_case', 'deaths ', 'type']].copy()

# This line might get dropped
new.astype({'res_case': 'int32'}).dtypes
new.astype({'staff_case': 'int32'}).dtypes
new.astype({'deaths ': 'int32'}).dtypes

new.rename(columns={"deaths ": "deaths"})
new['Total_Case'] = new['res_case'] + new['staff_case']
# Explicitly set date field
#new['Date'] = pd.to_datetime(new['Date'])

new.head()

new['pct_change_cases'] = new.groupby(['setting'])['Total_Case'].apply(lambda x: x.pct_change())
#new['pct_change_deaths'] = new.groupby(['location'])['deaths'].apply(lambda x: x.pct_change())
print(new.tail())

# Convert percentage to expected format
new['pct_change_cases']= np.round(new['pct_change_cases'] *100, decimals = 1)
new['pct_change_cases'] = new['pct_change_cases'].fillna(0)
#new['pct_change_deaths']= np.round(new['pct_change_deaths'] *100, decimals = 1)
new.tail(50)


# Drop NA on percent changes
#new.dropna()
#new.dropna(subset=['pct_change_cases'], inplace=True)
new.dropna(subset=['setting'], inplace=True)

# Select values for today
dval= datetime.today().strftime("%Y-%m-%d")
query = (new['Date'] == dval) 
new=new.loc[query]
new.to_csv('./content/output.csv')
