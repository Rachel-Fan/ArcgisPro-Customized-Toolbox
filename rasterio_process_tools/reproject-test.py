import arcpy
import os

# User-specified input and output paths
input_tif = r"D:\Eelgrass_Classified_from_Metashape\Alaska\Fishegg\2019\FI_AK_19_Clipped.tif"  # Change this
output_tif = r"D:\Eelgrass_Classified_from_Metashape\UTM\Alaska\FI_AK_19_Clipped_utm8n.tif"  # Change this

# Ensure output directory exists
output_dir = os.path.dirname(output_tif)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define target projection (UTM Zone 8N: EPSG 32608)
target_epsg = 32608
target_spatial_ref = arcpy.SpatialReference(target_epsg)

# Ensure the raster has a valid projection
desc = arcpy.Describe(input_tif)
if desc.spatialReference is None or desc.spatialReference.name == "Unknown":
    print(f"⚠️ Input raster has no projection! Defining as WGS84.")
    arcpy.DefineProjection_management(input_tif, arcpy.SpatialReference(4326))  # Assign WGS84 if undefined

# Get input raster cell size
try:
    cell_size_x = float(arcpy.GetRasterProperties_management(input_tif, "CELLSIZEX").getOutput(0))
    cell_size_y = float(arcpy.GetRasterProperties_management(input_tif, "CELLSIZEY").getOutput(0))
except:
    print("❌ Error: Unable to retrieve cell size. Exiting.")
    exit()

# Set environment settings
arcpy.env.outputCoordinateSystem = target_spatial_ref  # Set output spatial reference
arcpy.env.cellSize = cell_size_x  # Maintain same cell size
arcpy.env.compression = "NONE"  # No compression

# Use CopyRaster with detailed parameters
print(f"🚀 Copying & Reprojecting: {input_tif} → {output_tif}")

arcpy.management.CopyRaster(
    in_raster=input_tif,
    out_rasterdataset=output_tif,
    format="TIFF",             # Ensures output is GeoTIFF
    pixel_type="32_BIT_FLOAT",  # Preserves precision
    colormap_to_RGB="NONE"      # Keeps original format
)

print(f"✅ Copy & Reprojection Complete: {output_tif}")
