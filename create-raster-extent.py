import os
import arcpy
from arcpy.sa import *

def set_environment(workspace, overwrite):
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = overwrite

def raster_to_polygon(input_raster, output_polygon):
    arcpy.RasterDomain_3d(input_raster, output_polygon, "POLYGON")

def process_raster(input_raster, output_raster_path):
    output_raster = Raster(input_raster) * 0 + 1
    output_raster.save(output_raster_path)

def extract_prefix(input_raster):
    basename = os.path.basename(input_raster)
    prefix = basename.split("_", 2)[0]  # Extracting the substring before the third underscore
    return prefix

def main(input_raster, output_folder):
    prefix = extract_prefix(input_raster)
    print('prefix is ', prefix)
    temp_folder = os.path.join(output_folder, f"temp_{prefix}")

    set_environment(temp_folder, True)

    output_raster_path = os.path.join(temp_folder, "output_raster.tif")
    output_polygon = os.path.join(temp_folder, "input_raster_extent.shp")

    process_raster(input_raster, output_raster_path)
    print('process raster geoprocessing is done' )
    raster_to_polygon(output_raster_path, output_polygon)

    print("Geoprocessing complete.")

if __name__ == "__main__":
    input_raster = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2019\NC_19_Clipped.tif"
    output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\2019\Washington"

    main(input_raster, output_folder)
