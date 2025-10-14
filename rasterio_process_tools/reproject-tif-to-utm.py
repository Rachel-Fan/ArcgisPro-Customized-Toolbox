import arcpy
import os
import shutil
import time

def find_tif_files(root_dir):
    """Recursively find all .tif files in the given directory and subdirectories."""
    print("\n🔍 Searching for .tif files...")
    tif_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower().endswith(".tif"):
                tif_files.append(os.path.join(dirpath, file))
    print(f"✅ Found {len(tif_files)} .tif files.\n")
    return tif_files

def reproject_tif(input_tif, input_root, output_root, target_epsg=32608):
    """Reproject the given .tif file to UTM Zone 8N and save with _utm8n suffix while keeping the same folder structure."""
    try:
        # Get original file name (without extension) and add "_utm8n"
        base_name = os.path.splitext(os.path.basename(input_tif))[0] + "_utm8n.tif"

        # Determine the relative path of the input file
        relative_path = os.path.relpath(input_tif, input_root)
        relative_folder = os.path.dirname(relative_path)

        # Construct the corresponding output folder path
        output_tif_folder = os.path.join(output_root, relative_folder)
        os.makedirs(output_tif_folder, exist_ok=True)  # Ensure the output directory exists

        # Define output file path with "_utm8n" suffix
        output_tif = os.path.join(output_tif_folder, base_name)

        # Define the target spatial reference (UTM Zone 8N)
        target_spatial_ref = arcpy.SpatialReference(target_epsg)

        # Ensure the raster has a valid projection
        desc = arcpy.Describe(input_tif)
        if desc.spatialReference is None or desc.spatialReference.name == "Unknown":
            print(f"⚠️ Input raster has no projection! Defining as WGS84.")
            arcpy.DefineProjection_management(input_tif, arcpy.SpatialReference(4326))  # Assign WGS84 if undefined

        # Get original cell size from input raster
        try:
            cell_size_x = float(arcpy.GetRasterProperties_management(input_tif, "CELLSIZEX").getOutput(0))
            cell_size_y = float(arcpy.GetRasterProperties_management(input_tif, "CELLSIZEY").getOutput(0))
        except:
            print(f"❌ Error: Unable to retrieve cell size for {input_tif}. Skipping.")
            return

        # Set environment settings
        arcpy.env.outputCoordinateSystem = target_spatial_ref  # Set output spatial reference
        arcpy.env.cellSize = cell_size_x  # Maintain same cell size
        arcpy.env.compression = "NONE"  # No compression

        # Perform the reprojection using CopyRaster
        print(f"🚀 Copying & Reprojecting: {input_tif} → {output_tif}")
        arcpy.management.CopyRaster(
            in_raster=input_tif,
            out_rasterdataset=output_tif,
            format="TIFF",             # Ensures output is GeoTIFF
            pixel_type="32_BIT_FLOAT",  # Preserves precision
            colormap_to_RGB="NONE"      # Keeps original format
        )
        print(f"✅ Copy & Reprojection Complete: {output_tif}")

    except Exception as e:
        print(f"❌ Error reprojecting {input_tif}: {e}")

def copy_vector_files(input_root, output_root, extensions=(".dbf", ".prj", ".shp", ".shx")):
    """Copy vector files (.dbf, .prj, .shp, .shx) from input folders to corresponding output folders."""
    print("\n🔍 Searching for vector files (.dbf, .prj, .shp, .shx)...")
    file_count = 0

    for dirpath, _, filenames in os.walk(input_root):
        for file in filenames:
            if file.lower().endswith(extensions):
                # Construct full source file path
                source_file = os.path.join(dirpath, file)

                # Determine relative path and corresponding output folder
                relative_path = os.path.relpath(source_file, input_root)
                output_folder = os.path.join(output_root, os.path.dirname(relative_path))
                
                # Ensure the corresponding output folder exists
                os.makedirs(output_folder, exist_ok=True)

                # Copy the vector file
                destination_file = os.path.join(output_folder, file)
                shutil.copy2(source_file, destination_file)

                file_count += 1
                print(f"✅ Copied: {source_file} → {destination_file}")

    print(f"✅ Total vector files copied: {file_count}\n")

def main(input_root, output_root):
    """Find and reproject all .tif files and copy vector files while preserving folder structure."""
    arcpy.env.overwriteOutput = True  # Allow overwriting existing files

    print("\n🚀 Processing Started...")
    start_time = time.time()

    # Step 1: Reproject all .tif files
    tif_files = find_tif_files(input_root)
    if not tif_files:
        print("⚠️ No .tif files found.")
    else:
        for index, tif in enumerate(tif_files, start=1):
            print(f"\n📌 Processing {index}/{len(tif_files)}: {tif}")
            reproject_tif(tif, input_root, output_root)

    # Step 2: Copy vector files (.dbf, .prj, .shp, .shx)
    copy_vector_files(input_root, output_root)

    # End timer
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Convert to hours, minutes, seconds
    hours, remainder = divmod(int(elapsed_time), 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"\n✅ Processing completed in {hours} hours {minutes} minutes {seconds} seconds!")


# Example usage
if __name__ == "__main__":
    input_directory = r"D:\Eelgrass_Classified_from_Metashape\BC"  
    output_directory = r"D:\Eelgrass_Classified_from_Metashape\UTM\BC"  

    main(input_directory, output_directory)
