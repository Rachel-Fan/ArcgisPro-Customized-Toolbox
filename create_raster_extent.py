import os
import arcpy
from arcpy.sa import *

# Define input and output parameters
arcpy.env.overwriteOutput = True

def set_environment(workspace, overwrite):
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = overwrite

def raster_to_polygon(input_raster, output_polygon):
    arcpy.RasterDomain_3d(input_raster, output_polygon, "POLYGON")

def process_raster(input_raster, output_raster_path):
    # Ensure that the output directory exists
    output_folder = os.path.dirname(output_raster_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process the raster
    output_raster = Raster(input_raster) * 0 + 1
    output_raster.save(output_raster_path)

def extract_prefix(input_raster):
    basename = os.path.basename(input_raster)
    parts = basename.split("_")
    prefix = "_".join(parts[:2])  # Join the first two parts with an underscore
    
    return prefix

def perform_raster_calculator(input_raster, output_raster):
    # Set environment settings to ensure extent matching
    arcpy.env.extent = arcpy.Describe(input_raster).extent
    
    # Perform raster calculator operation
    expression = 'Con(IsNull("{}"), 0, 1)'.format(input_raster)
    arcpy.gp.RasterCalculator_sa(expression, output_raster)

def main(input_raster, output_folder):
    prefix = extract_prefix(input_raster)
    temp_folder = os.path.join(output_folder, f"temp_{prefix}")
    print('prefix is', prefix)

    set_environment(temp_folder, True)

    output_raster_path = os.path.join(temp_folder, "output_raster.tif")
    output_polygon = os.path.join(temp_folder, "input_raster_extent.shp")
    output_index_tif = os.path.join(temp_folder, "index_tif.shp")

    process_raster(input_raster, output_raster_path)
    raster_to_polygon(output_raster_path, output_polygon)
    perform_raster_calculator(output_polygon, output_index_tif)
    print('')

#if __name__ == "__main__":

print('tool starts')
input_raster = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2019\NC_19_Clipped.tif"
output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\2019\Washington"

main(input_raster, output_folder)
print("Geoprocessing complete.")
