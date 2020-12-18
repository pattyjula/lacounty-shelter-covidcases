#!/usr/bin/env python
# coding: utf-8


from arcgis.gis import GIS
from time import sleep

#gis = GIS("home")
# LAPD Login
gispd = GIS("", username="", password="")
# LAHUB log in
gis = GIS("", username="", password="%")
# LAPD COVID19 log in
giscv = GIS("", username="", password="")

data_file = r'./content/shelter_cases.zip'
 
# Homeless shelters - JRIC
lapd_city_csv = giscv.content.get('27e19c52976a4462aa66c8825f44dafd')
# Call the update method to replace/overwrite it with the zip file from disk
lapd_city_csv.update({}, data_file)
#print(help(lapd_city_csv.publish))
# Update feature layer, must uncheck to disable editing
lapd_city_csv.publish(overwrite=True)

# Homeless shelters - PD
lapd_city_csv = gispd.content.get('b4a99161a90b4ada9ab8102f42627312')
# Call the update method to replace/overwrite it with the zip file from disk
lapd_city_csv.update({}, data_file)
#print(help(lapd_city_csv.publish))
# Update feature layer, must uncheck to disable editing
lapd_city_csv.publish(overwrite=True)

print("End of AGOL file")
