import arcpy
import os
arcpy.env.overwriteOutput = True

def erase_and_merge(extent_shapefile, attribute_area_shapefile, output_folder):
    # Ensure the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Output shapefile paths
    dissolved_attribute_area = os.path.join(output_folder, "dissolved_attribute_area.shp")
    erased_small_area = os.path.join(output_folder, "erased_small_area.shp")
    output_shapefile = os.path.join(output_folder, "merged_shapefile.shp")

    # Dissolve attribute_area_shapefile
    arcpy.Dissolve_management(attribute_area_shapefile, dissolved_attribute_area)

    # Add a new field "Seagrass" with a value of 1 to the dissolved attribute area shapefile
    arcpy.AddField_management(dissolved_attribute_area, "Seagrass", "SHORT")
    arcpy.CalculateField_management(dissolved_attribute_area, "Seagrass", 1)

    # Erase overlapping area from extent shapefile
    arcpy.Erase_analysis(extent_shapefile, dissolved_attribute_area, erased_small_area)

    # Add a new field "Seagrass" with a value of 0 to the erased_small_area shapefile
    arcpy.AddField_management(erased_small_area, "Seagrass", "SHORT")
    arcpy.CalculateField_management(erased_small_area, "Seagrass", 0)

    # Merge extent and updated small area shapefiles
    arcpy.Merge_management([dissolved_attribute_area, erased_small_area], output_shapefile)

    print("Erase, dissolve, merge, and field addition completed successfully.")

if __name__ == "__main__":
    # Input shapefiles
    extent_shapefile = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021\Tool_Temp\output_polygon.shp"
    attribute_area_shapefile = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NC21_Eelgrass_New\NC21_Eelgrass_New.shp"
    
    # Output shapefile
    output_shapefile = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021\Tool_Temp\output_polygon.shp\index_extent.shp"

    # Output folder
    output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021\Tool_Temp"
    
    # Erase and merge shapefiles
    erase_and_merge(extent_shapefile, attribute_area_shapefile, output_folder)
