import arcpy
from arcpy import env
from arcpy.sa import *

def create_tiles_from_raster(input_raster, output_shapefile, tile_size):
    # Set environment settings
    env.workspace = arcpy.Describe(input_raster).path
    env.overwriteOutput = True

    # Get raster extent
    desc = arcpy.Describe(input_raster)
    extent = desc.extent

    # Convert YMin to float
    y_min = float(extent.YMin)

    # Define coordinates for the fishnet extent
    origin_coord = f"{extent.XMin} {y_min}"
    y_axis_coord = f"{extent.XMin} {y_min + tile_size}"
    corner_coord = f"{extent.XMax} {extent.YMax}"
    
    # Create a Fishnet grid
    arcpy.CreateFishnet_management(output_shapefile, origin_coord, y_axis_coord, tile_size, tile_size, "0", "0", corner_coord, "NO_LABELS", input_raster)


    print("***************output fishnet (tile) created *******************")
    print(output_shapefile)

# Example usage:
input_raster = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NorthCov21_Clipped.tif"
output_shapefile = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2020\Autoclip512\tile_index.shp"
tile_size = 512
create_tiles_from_raster(input_raster, output_shapefile, tile_size)
