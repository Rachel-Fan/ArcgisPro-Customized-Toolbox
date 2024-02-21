import arcpy
from arcpy.sa import *
import os

import arcpy
from arcpy.sa import *
import csv
import sys
import os
from os import path
# Check Spatial Analyst extention
arcpy.CheckOutExtension("Spatial")
#Define input and output parameters
arcpy.env.overwriteOutput = True

def clip_raster_by_tile(input_raster, tile_shapefile, output_folder):
    # Check out Spatial Analyst extension
    arcpy.CheckOutExtension("Spatial")

    # Create output folders if they don't exist
    output_drone_image = os.path.join(output_folder, "drone_image")
    if not os.path.exists(output_drone_image):
        os.makedirs(output_drone_image)

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
            output_raster_tif = os.path.join(output_drone_image, f"clipped_raster_{tile_id}.tif")
            mask.save(output_raster_tif)
            
            print("***************output raster (TIFF) created *******************")
            print(output_raster_tif)

            # Convert TIFF to PNG and save in "png" folder
            output_raster_png = os.path.join(output_png, f"clipped_raster_{tile_id}.png")
            arcpy.management.CopyRaster(output_raster_tif, output_raster_png, "","0","0","","ColormapToRGB","8_BIT_UNSIGNED","","", format = "PNG")
            
            
            print("***************output raster (PNG) created *******************")
            print(output_raster_png)
            
            arcpy.env.extent = None

if __name__ == "__main__":
    # Set input parameters
    input_raster = r"C:\Users\Rachel\Documents\Seagrass\Dataset\Downloaded_Tif_image\Washington\North_Cove\2020\NorthCove20_Clipped.tif"
    #input_raster = r"C:\Users\Rachel\Documents\Seagrass\Dataset\Temp\NC20_Eelgrass_1_0.tif"

    tile_shapefile = r"C:\Users\Rachel\Documents\Seagrass\Dataset\Temp\NorthCov20_tiles_100.shp"
    output_folder = r"C:\Users\Rachel\Documents\Seagrass\Dataset\Temp\NC20_cs20\Clipped_0220\Drone"

    print("Parameters read. Start processing... ")
    # Call the function to clip raster by each tile
    clip_raster_by_tile(input_raster, tile_shapefile, output_folder)
    print("All done")
