import arcpy
from arcpy import env
from arcpy.sa import *

def create_tiles_from_raster(input_raster, output_shapefile, tile_size):
    # Set environment settings
    env.workspace = arcpy.Describe(input_raster).path
    env.overwriteOutput = True

    # Create a Fishnet grid
    arcpy.CreateFishnet_management(output_shapefile, "extent_of_raster", "0", "0", tile_size, tile_size, "0", "0", "extent_of_raster", "NO_LABELS", input_raster)

    # Buffer the points to create squares of desired size
    arcpy.Buffer_analysis("tile_points.shp", "tile_buffers.shp", tile_size / 2)

    # Use the buffered polygons to clip the raster
    arcpy.Clip_management(input_raster, "", "clipped_raster.tif", "tile_buffers.shp", "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

    # Iterate through clipped rasters and export as PNG
    with arcpy.da.SearchCursor(output_shapefile, ["OID@", "SHAPE@"]) as cursor:
        for row in cursor:
            output_png = "tile_" + str(row[0]) + ".png"
            arcpy.RasterToOtherFormat_conversion("clipped_raster.tif", output_png, "PNG")

# Example usage:
input_raster = "your_raster.tif"
output_shapefile = "tile_index.shp"
tile_size = '512'
create_tiles_from_raster(input_raster, output_shapefile, tile_size)
