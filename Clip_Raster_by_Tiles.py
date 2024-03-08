import arcpy
from arcpy.sa import *
import os

import arcpy
from arcpy.sa import *
import os
from os import path
import time

# Check Spatial Analyst extention
arcpy.CheckOutExtension("Spatial")
#Define input and output parameters
arcpy.env.overwriteOutput = True

def clip_raster_by_tile(input_raster, tile_shapefile, DateSource ,output_folder):
    # Check out Spatial Analyst extension
    arcpy.CheckOutExtension("Spatial")

    # Create output folders if they don't exist
    output_tif = os.path.join(output_folder, "tif")
    if not os.path.exists(output_tif):
        os.makedirs(output_tif)

    output_png = os.path.join(output_folder, "png")
    if not os.path.exists(output_png):
        os.makedirs(output_png)

    # Iterate through each feature (tile) in the shapefile
    with arcpy.da.SearchCursor(tile_shapefile, ['OID@', 'SHAPE@']) as cursor:
        for row in cursor:
            tile_id = row[0]
            tile_geometry = row[1]
            print("****Start clipping******")
            print(tile_id)
            
            arcpy.env.extent = tile_geometry.extent
            mask = arcpy.sa.ExtractByMask(input_raster, tile_geometry)
            
            # Save clipped raster as TIFF in "drone_image" folder
            output_raster_tif = os.path.join(output_tif, f"{DateSource}_{tile_id}.tif")
            mask.save(output_raster_tif)
            
            print("***************output raster (TIFF) created *******************")
            print(output_raster_tif)

            # Convert TIFF to PNG and save in "png" folder
            output_raster_png = os.path.join(output_png, f"{DateSource}_{tile_id}.png")
            arcpy.management.CopyRaster(output_raster_tif, output_raster_png, "","0","0","","ColormapToRGB","8_BIT_UNSIGNED","","", format = "PNG")
            
            
            print("***************output raster (PNG) created *******************")
            print(output_raster_png)
            
            arcpy.env.extent = None

if __name__ == "__main__":
    
    # Capture start time
    start_time = time.time()
    print("Start:", time.ctime())  # Track progress
    
    # Set input parameters
    input_raster = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NorthCov21_Clipped.tif"
    index_raster = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021\index_raster.tif"

    tile_shapefile = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2020\Autoclip512\tile_index_selected.shp"
    
    DataSource = 'NC_21'
    
    output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021"

    print("Parameters read. Start processing... ")
    
    # Create output folders if they don't exist
    output_drone_image = os.path.join(output_folder, "drone_image")
    if not os.path.exists(output_drone_image):
        os.makedirs(output_drone_image)

    output_index = os.path.join(output_folder, "index_tile")
    if not os.path.exists(output_index):
        os.makedirs(output_index)


    # Call the function to clip raster by each tile
    clip_raster_by_tile(input_raster, tile_shapefile, DataSource, output_drone_image)
    print("Drone images are clipped:", time.ctime())
    clip_raster_by_tile(index_raster, tile_shapefile, DataSource,  output_index)
    print("Index images are clipped:", time.ctime())
    
    print("All done:", time.ctime())

    # Calculate total processing time
    end_time = time.time()
    total_processing_time = end_time - start_time

    # Print total processing time
    print(f"Total processing time: {total_processing_time} seconds.")