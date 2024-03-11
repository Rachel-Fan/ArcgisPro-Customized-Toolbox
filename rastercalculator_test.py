import arcpy

NorthCov21_Clipped = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NorthCov21_Clipped.tif"
NC21_Eelgrass_New = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NC21_Eelgrass_New_2.tif"

output_tif = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NC_rc_TOOL.tif"

# Set environment settings to ensure extent matching
arcpy.env.extent = arcpy.Describe(NorthCov21_Clipped).extent

# Perform raster calculator operation
arcpy.gp.RasterCalculator_sa('Con(IsNull(NC21_Eelgrass_New), 0, 1)', output_tif)

print('Raster calculator processing completed')