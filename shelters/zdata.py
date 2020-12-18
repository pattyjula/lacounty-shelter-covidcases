import os
import zipfile
import shutil

myfile="./content/shelter_cases.zip"

## If file exists, delete it ##
if os.path.isfile(myfile):
    os.remove(myfile)
else:    ## Show an error ##
    print("Error: %s file not found")

loc = './content'
pth = os.chdir(loc)

print('creating archive')
zf = zipfile.ZipFile('shelter_cases.zip', mode='w')
try:
    print('adding files')
    zf.write('congregate_data2.cpg')
    zf.write('congregate_data2.shx')
    zf.write('congregate_data2.shp')
    zf.write('congregate_data2.dbf')
    zf.write('congregate_data2.prj')
finally:
    print('closing')
    zf.close()

