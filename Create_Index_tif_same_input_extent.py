import os
import arcpy
from arcpy.sa import *
import glob

def set_environment(workspace, overwrite):
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = overwrite
    
def extract_prefix(input_raster):
    basename = os.path.basename(input_raster)
    parts = basename.split("_")
    prefix = "_".join(parts[:2])  # Join the first two parts with an underscore
    print('prefix is ',prefix)
    return prefix

def get_cell_size(input_raster):
    desc = arcpy.Describe(input_raster)
    cell_size = desc.children[0].meanCellHeight
    print('cell size is', cell_size)
    return cell_size

def convert_shapefile_to_tif(input_shapefile, output_raster, cell_size, bpp=8):
    arcpy.env.workspace = os.path.dirname(output_raster)
    arcpy.conversion.PolygonToRaster(input_shapefile, "FID", os.path.basename(output_raster), "CELL_CENTER", "NONE", cell_size)
    print('covert shp to tif done')

def perform_raster_calculator(input_raster, index_raster, output_raster):
    arcpy.env.workspace = None
    arcpy.env.extent = arcpy.Describe(input_raster).extent
    expression = 'Con(IsNull("{}"), 0, 1)'.format(index_raster.replace("\\", "/"))
    arcpy.gp.RasterCalculator_sa(expression, output_raster)
    print('raster calculator is done. Index raster is at', output_raster)

def main(input_folder, output_folder):
    index_tif_folder = os.path.join(output_folder, "Index_tif")
    temp_folder = os.path.join(output_folder, "Temp")
    os.makedirs(index_tif_folder, exist_ok=True)
    os.makedirs(temp_folder, exist_ok=True)

    tif_files = glob.glob(os.path.join(input_folder, '**/*.tif'), recursive=True)
    shp_files = glob.glob(os.path.join(input_folder, '**/*.shp'), recursive=True)

    for input_raster in tif_files:
        matching_shp = next((shp for shp in shp_files if extract_prefix(shp) == extract_prefix(input_raster)), None)
        if not matching_shp:
            continue  # No matching shapefile found, skip to next raster

        prefix = extract_prefix(input_raster)
        output_raster = os.path.join(temp_folder, f"{prefix}_{year[2:]}_output_raster.tif")
        output_index_tif = os.path.join(index_tif_folder, f"{prefix}_{year[2:]}_index_tif.tif")

        set_environment(temp_folder, True)
        cell_size = get_cell_size(input_raster)
        convert_shapefile_to_tif(matching_shp, output_raster, cell_size)
        perform_raster_calculator(input_raster, output_raster, output_index_tif)

if __name__ == "__main__":
    year = "2022"
    input_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Alaska"
    output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Alaska\{}".format(year)
    main(input_folder, output_folder)
    print('Index rasters are created')