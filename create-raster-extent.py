import arcpy
from arcpy.sa import *

# Set environment settings
arcpy.env.workspace = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021\Tool_Temp"
arcpy.env.overwriteOutput = True

# Input raster file
input_raster = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NorthCov21_Clipped.tif"

# Step 1: Use raster calculator to set all values to one
output_raster = Raster(input_raster) * 0 + 1
output_raster.save(r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021\Tool_Temp\output_raster.tif")

# Step 2: Run raster to polygon conversion to create a shapefile
output_polygon = "input_raster_extent.shp"
arcpy.RasterDomain_3d("output_raster.tif", output_polygon, "POLYGON")

print("Geoprocessing complete.")
