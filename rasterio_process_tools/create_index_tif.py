import os
import arcpy
from arcpy.sa import *
import glob
import time

def set_environment(workspace, input_raster):
    """Sets the environment with the correct workspace and raster properties."""
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True
    arcpy.env.snapRaster = input_raster
    arcpy.env.extent = arcpy.Describe(input_raster).extent  # Match extent

def extract_prefix(input_raster):
    """Extracts prefix from file name."""
    basename = os.path.basename(input_raster)
    parts = basename.split("_")
    prefix = "_".join(parts[:2])
    print('Prefix:', prefix)
    return prefix

def get_cell_size(input_raster):
    """Gets the correct cell size from the raster dataset."""
    desc = arcpy.Describe(input_raster)
    
    # Check if the raster has children (for multi-band rasters)
    if hasattr(desc, 'children') and desc.children:
        cell_size = desc.children[0].meanCellHeight
    else:
        # Use Raster properties for single-band rasters
        raster = arcpy.Raster(input_raster)
        cell_size = raster.meanCellHeight
    
    print('Cell size:', cell_size)
    return cell_size


def match_projection(input_shapefile, input_raster, temp_folder):
    """Ensures the shapefile projection matches the input raster."""
    sr_raster = arcpy.Describe(input_raster).spatialReference
    sr_shapefile = arcpy.Describe(input_shapefile).spatialReference

    if sr_raster.name != sr_shapefile.name:
        reprojected_shapefile = os.path.join(temp_folder, "reprojected.shp")
        arcpy.Project_management(input_shapefile, reprojected_shapefile, sr_raster)
        print(f'Reprojected {input_shapefile} to match raster.')
        return reprojected_shapefile
    return input_shapefile

def convert_shapefile_to_tif(input_shapefile, output_raster, cell_size, input_raster):
    """Converts a shapefile to a raster TIFF with the same alignment as the input raster."""
    arcpy.env.extent = arcpy.Describe(input_raster).extent  # Match original extent
    arcpy.conversion.PolygonToRaster(input_shapefile, "FID", output_raster, "MAXIMUM_AREA", "NONE", cell_size)
    print(f'Converted {input_shapefile} to {output_raster}')

def perform_raster_calculator(input_raster, index_raster, output_raster):
    """Creates a binary raster (1 for presence, 0 for no data) matching input raster dimensions."""
    expression = 'Con(IsNull("{}"), 0, 1)'.format(index_raster.replace("\\", "/"))

    arcpy.gp.RasterCalculator_sa(expression, output_raster)
    print(f'Raster calculator done. Index raster saved at {output_raster}')

def main(input_folder, output_folder, year):
    """Processes all rasters in the input folder, generating index rasters."""
    index_tif_folder = os.path.join(output_folder, "Index_tif")
    temp_folder = os.path.join(output_folder, "Temp")
    os.makedirs(index_tif_folder, exist_ok=True)
    os.makedirs(temp_folder, exist_ok=True)

    tif_files = glob.glob(os.path.join(input_folder, '*.tif'))
    shp_files = glob.glob(os.path.join(input_folder, '*.shp'))

    for input_raster in tif_files:
        print('Processing input raster:', input_raster)
        matching_shp = next((shp for shp in shp_files if extract_prefix(shp) == extract_prefix(input_raster)), None)

        if not matching_shp:
            print('No matching shapefile found for', input_raster)
            continue

        prefix = extract_prefix(input_raster)
        output_raster = os.path.join(temp_folder, f"{prefix}_{year[2:]}_output_raster.tif")
        output_index_tif = os.path.join(index_tif_folder, f"{prefix}_{year[2:]}_index_tif.tif")

        set_environment(temp_folder, input_raster)
        cell_size = get_cell_size(input_raster)
        matching_shp = match_projection(matching_shp, input_raster, temp_folder)
        convert_shapefile_to_tif(matching_shp, output_raster, cell_size, input_raster)
        perform_raster_calculator(input_raster, output_raster, output_index_tif)

        print(f'Final index raster created at {output_index_tif}')

import os
import time

if __name__ == "__main__":
    start_time = time.time()
    base_folder = r"D:\Eelgrass_Classified_from_Metashape\UTM\Washington"
    years = ["2019", "2020", "2021", "2022", "2024"]  # List of years to process

    for year in years:
        for folder in os.listdir(base_folder):
            input_folder = os.path.join(base_folder, folder, year)
            output_folder = os.path.join(
                r"D:\Eelgrass_processed_images_2025\ModelData\Alaska_0310_reproj", year
            )

            if os.path.isdir(input_folder):
                print(f"Processing {input_folder} for year {year}")
                main(input_folder, output_folder, year)

    end_time = time.time()
    print("All specified index rasters for all years are created.")

    # Convert elapsed time into H:M:S
    elapsed_time = int(end_time - start_time)
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Build a human-readable string that skips zero values
    parts = []
    if hours > 0:
        parts.append(f"{hours} hours")
    if minutes > 0:
        parts.append(f"{minutes} minutes")
    if seconds > 0 or not parts:  # Always show seconds if everything else is 0
        parts.append(f"{seconds} seconds")

    print("Execution time: " + " ".join(parts))
