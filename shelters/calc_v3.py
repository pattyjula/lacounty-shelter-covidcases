import arcpy

# Local variables:
arcpy.env.workspace = "E:/batch/dashboard_covid19/shelters"
ws = arcpy.env.workspace
arcpy.env.overwriteOutput = True
LAneighborhood_total = "content/congregate_data.shp"
LAneighborhood_total__2_ = LAneighborhood_total
LAneighborhood_total__4_ = LAneighborhood_total__2_
LAneighborhood_total__3_ = LAneighborhood_total__4_
LAneighborhood_total2 = "content/congregate_data2.shp"
# Process: Define Projection
arcpy.DefineProjection_management(LAneighborhood_total, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
# Process: Add Field
arcpy.AddField_management(LAneighborhood_total, "UPDATE", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field

arcpy.CalculateField_management(LAneighborhood_total__2_, "UPDATE", expression="datetime.datetime.strptime(!Date!,'%Y-%m-%d') + datetime.timedelta(hours=24) ", expression_type="PYTHON", code_block="")

def calcdata(fld, oldfld, fa):
    arcpy.AddField_management(LAneighborhood_total, fld, "SHORT", "", "", "", fa, "", "", "")

    arcpy.CalculateField_management(LAneighborhood_total, fld, expression=oldfld, expression_type="PYTHON", code_block="")

calcdata("ResCase", '!res_case!', 'Resident Case Count')
calcdata("StaffCase", '!staff_case!', 'Staff Case Count')
calcdata("TotCase", '!Total_Case!', 'Total Case Count')


# Process: Add Field - pct change
arcpy.AddField_management(LAneighborhood_total, "Prct_Chnge", "FLOAT", 5, 1, "", "Percent Change Cases (7 day)",)

# Process: Calculate Field

arcpy.CalculateField_management(LAneighborhood_total__2_, "Prct_Chnge", expression="!pct_change!", expression_type="PYTHON", code_block="")

calcdata("Death", '!deaths!', 'Death Count')

with arcpy.da.UpdateCursor(LAneighborhood_total__2_, ["Prct_Chnge"]) as cursor:
    for row in cursor:
        if row[0] == 0.0:
            row[0] = 0
            cursor.updateRow(row)

print("Processing complete")
# Process: Delete Field
arcpy.DeleteField_management(LAneighborhood_total__4_, "Unnamed__0;Notes;setting;type;Date_;Date;obs;res_case;staff_case;deaths;Total_Case;pct_change")

arcpy.CopyFeatures_management(LAneighborhood_total, LAneighborhood_total2, "", "0", "0", "0")
arcpy.DeleteField_management(LAneighborhood_total2, "Unnamed__0")
