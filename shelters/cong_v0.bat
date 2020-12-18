@Echo ON
REM setlocal enableextensions
SET LOGFILE="P:\ITD\AREA-ADSD CO-ADSD GIS\Projects\incidents\COVID19\logs\covid_shelters.log"
REM call :sub > %LOGFILE% 

REM Web scraping
"C:\Users\Administrator\anaconda3\python.exe" "congregate_v2.py"

REM Calc total and % change
"C:\Users\Administrator\anaconda3\python.exe" "pct_v1.py"

REM Merge counts table to Homeless Locations shapefile

"C:\Users\Administrator\anaconda3\python.exe" "merge_v0.py"

REM Cleaning up fields and adding one to Date value

"E:\Python27\ArcGIS10.6\python2.exe" "calc_v3.py"

REM Creating zip file of finalized shapefile

"C:\Users\Administrator\anaconda3\python.exe" "zdata.py"

REM Write to AGOL

"C:\Users\Administrator\anaconda3\python.exe" "shelter_agol_v0.py"

pause
