import pandas as pd
import geopandas

df_cong = pd.read_csv("./content/output.csv")
'''
Join Data to shapefile
'''

import geopandas
#url = "http://s3-us-west-2.amazonaws.com/boundaries.latimes.com/archive/1.0/boundary-set/la-county-neighborhoods-current.geojson"
gdf = geopandas.read_file("P:/ITD/AREA-ADSD CO-ADSD GIS/Projects/incidents/COVID19/shelters/Homeless_Locations.shp")
#gdf = geopandas.read_file(url)
#gdf.plot()

gdfNew = gdf.merge(df_cong, left_on='Location', right_on='setting', how='inner')

#gdfNew['Date'] = pd.to_datetime(gdfNew['Date']).dt.date
gdfNew[["Date"]] = gdfNew[["Date"]].astype(str)
# gdfNew[["deaths"]] = gdfNew[["deaths"]].astype(int)
# gdfNew[["res_case"]] = gdfNew[["res_case"]].astype(int)  
# gdfNew[["staff_case"]] = gdfNew[["staff_case"]].astype(int) 


#gdfNew[["count"]] = gdfNew[["count"]].astype(int) 
# Export to shapefile
gdfNew.to_file(driver = 'ESRI Shapefile', filename= './content/congregate_data.shp')