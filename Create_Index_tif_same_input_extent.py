import os
import arcpy
from arcpy.sa import *

def set_environment(workspace, overwrite):
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = overwrite
    
def extract_prefix(input_raster):
    basename = os.path.basename(input_raster)
    parts = basename.split("_")
    prefix = "_".join(parts[:2])  # Join the first two parts with an underscore
    
    return prefix

def get_cell_size(input_raster):
    # Get cell size of the input raster
    desc = arcpy.Describe(input_raster)
    cell_size = desc.children[0].meanCellHeight
    print('cell size is ', cell_size)
    return cell_size

def convert_shapefile_to_tif(input_shapefile, output_raster, cell_size, bpp=8):

    # Set environment workspace to output folder
    arcpy.env.workspace = os.path.dirname(output_raster)
    
    # Perform Polygon to Raster conversion
    arcpy.conversion.PolygonToRaster(input_shapefile, "FID", os.path.basename(output_raster), "CELL_CENTER", "NONE", cell_size)
    print('eelgrass extent tif is create at', output_raster)
    
    # Perform Polygon to Raster conversion
    #arcpy.conversion.PolygonToRaster(input_shapefile, "FID", output_raster, "CELL_CENTER", "NONE", cell_size)

    
    # Copy the raster to the desired output raster with specified bpp
    #arcpy.management.CopyRaster("temp_raster", output_raster, pixel_type="8_BIT_UNSIGNED" if bpp == 8 else "16_BIT_UNSIGNED" if bpp == 16 else "32_BIT_FLOAT")

    # Delete temporary raster
    #arcpy.management.Delete("temp_raster")
    
    #arcpy.FeatureToRaster_conversion(input_shapefile, "Value", output_raster)
    
def perform_raster_calculator(input_raster, index_raster, output_raster):
    # Set environment workspace to output folder
    arcpy.env.workspace = None
    
    # Set environment settings to ensure extent matching
    arcpy.env.extent = arcpy.Describe(input_raster).extent
    
    # Perform raster calculator operation
    expression = 'Con(IsNull("{}"), 0, 1)'.format(index_raster.replace("\\", "/"))
    print('express is', expression)
    arcpy.gp.RasterCalculator_sa(expression, output_raster)
    
    # Perform raster calculator operation
    #arcpy.gp.RasterCalculator_sa('Con(IsNull(index_raster), 0, 1)', output_raster)



def main(input_folder, output_folder):
    
    arcpy.env.workspace = output_folder
    
    # Find input raster (.tif) and shapefile (.shp) within input folder
    tif_files = [f for f in os.listdir(input_folder) if f.endswith('.tif')]
    shp_files = [f for f in os.listdir(input_folder) if f.endswith('.shp')]

    # Check if both raster and shapefile are found
    if len(tif_files) == 0 or len(shp_files) == 0:
        print("Error: Could not find required input files.")
        return

    input_raster = os.path.join(input_folder, tif_files[0])
    input_shp = os.path.join(input_folder, shp_files[0])
    print('input_raster is', input_raster)
    print('input_shapefile is ', input_shp)
    
    prefix = extract_prefix(input_shp)
    temp_folder = os.path.join(output_folder, f"temp_{prefix}")
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder) 
    print('prefix is', prefix)
    
    set_environment(temp_folder, True)

    output_raster = os.path.join(temp_folder, "output_raster_0312.tif")
    output_polygon = os.path.join(temp_folder, "input_raster_extent.shp")
    output_index_tif = os.path.join(output_folder, f"{prefix}_index_tif.tif")

    # process_raster(input_raster, output_raster_path)
    # raster_to_polygon(output_raster_path, output_polygon)
    cell_size = get_cell_size(input_raster)
    print('cell size is extracted. cell size is', cell_size)
    print("*****************************")
    convert_shapefile_to_tif(input_shp, output_raster, cell_size, bpp=8)
    print("convert shp to tif done")
    print("*****************************")

    print('raster calculator index raster is', output_raster)
    perform_raster_calculator(input_raster, output_raster,output_index_tif)
    print('raster calculator is done. Result is at ', output_index_tif)
    print("*****************************")

if __name__ == "__main__":
    input_folder = r"C:\Users\Rachel\Documents\Seagrass\Dataset\2019"
    #input_shp = r"C:\Users\Rachel\Documents\Seagrass\Dataset\2019\NC_19_Eelgrass.shp"
    output_folder = r"C:\Users\Rachel\Documents\Seagrass\Dataset\Script_0312" 
    main(input_folder, output_folder)
    print('Raster calculator processing completed')