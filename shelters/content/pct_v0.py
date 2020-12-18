#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime

# Set variables
df = pd.read_csv("./data/congregate_storage.csv", encoding='utf-8')#, index=False)
df['Date'] = pd.to_datetime(df['Date'])
df['day_of_week'] = df['Date'].dt.day_name()

# Create the data frame of the current day of the week
# Very important for the percent change
dval = datetime.today().strftime('%A')
df = df.loc[(df['day_of_week']== dval)] 

# Identify fields to use
new = df[['Date_', 'setting','res_case', 'staff_rate', 'deaths', 'type']].copy()

# This line might get dropped
new.astype({'cases': 'int32'}).dtypes
#new.astype({'deaths': 'int32'}).dtypes

# Explicitly set date field
new['Date'] = pd.to_datetime(new['Date'])


new['pct_change_cases'] = new.groupby(['location'])['cases'].apply(lambda x: x.pct_change())
new['pct_change_deaths'] = new.groupby(['location'])['deaths'].apply(lambda x: x.pct_change())
print(new.tail(5))

# Convert percentage to expected format
new['pct_change_cases']= np.round(new['pct_change_cases'] *100, decimals = 1)
new['pct_change_deaths']= np.round(new['pct_change_deaths'] *100, decimals = 1)

# Drop NA on percent changes
new.dropna()
new.dropna(subset=['pct_change_cases'], inplace=True)

# Select values for today
dval= datetime.today().strftime("%Y-%m-%d")
query = (new['Date'] == dval) 
new=new.loc[query]

# Export to CSV
new.to_csv("./data/neighborhood_storage_pctchange.csv", encoding='utf-8', index=False)

'''
Join Data to shapefile
'''

import geopandas
#url = "http://s3-us-west-2.amazonaws.com/boundaries.latimes.com/archive/1.0/boundary-set/la-county-neighborhoods-current.geojson"
gdf = geopandas.read_file("./data/LACity_communities.shp")
#gdf = geopandas.read_file(url)
gdf.plot()

gdfNew = gdf.merge(new, left_on='COMTY_NAME', right_on='location', how='inner')

# Data wrangling to get fields in proper format
gdfNew[["Date"]] = gdfNew[["Date"]].astype(str)
gdfNew[['case_count']] = gdfNew[['cases']].astype(int) 
gdfNew[['Cpct_chnge']] = gdfNew[['pct_change_cases']].astype(float)
gdfNew[['case_rate']] = gdfNew[['case_rate']].astype(float) 
gdfNew[['case_count']] = gdfNew[['deaths']].astype(int) 
gdfNew[['Dpct_chngeD']] = gdfNew[['pct_change_deaths']].astype(float)
gdfNew[['death_rate']] = gdfNew[['death_rate']].astype(float)

# Export to shapefile
gdfNew.to_file(driver = 'ESRI Shapefile', filename= './data/nghbrhd_data_pctchange.shp')




