import arcpy
import time

def select_intersecting_features(tile_shapefile, seagrass_shapefile, output_shapefile):
    # Make a layer from the input tile shapefile
    arcpy.MakeFeatureLayer_management(tile_shapefile, "tiles_lyr")

    # Select features from the tile shapefile that intersect with the seagrass shapefile
    arcpy.SelectLayerByLocation_management("tiles_lyr", "INTERSECT", seagrass_shapefile)

    # Copy the selected features to a new shapefile
    arcpy.CopyFeatures_management("tiles_lyr", output_shapefile)

    # Clean up
    arcpy.Delete_management("tiles_lyr")

# Example usage:
input_tile_shapefile = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2020\Autoclip512\tile_index.shp"
input_seagrass_shapefile = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NC21_Eelgrass_New\NC21_Eelgrass_New.shp"
output_shapefile = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2020\Autoclip512\tile_index_selected.shp"

select_intersecting_features(input_tile_shapefile, input_seagrass_shapefile, output_shapefile)
