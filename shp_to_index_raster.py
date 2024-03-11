import arcpy
import os

# Define input and output parameters
arcpy.env.overwriteOutput = True

def create_index_shapefile(input_folder, output_folder, input_raster_for_extent):
    # Get cell size of the input raster
    desc = arcpy.Describe(input_raster_for_extent)
    extent = desc.extent

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".shp"):
            # Construct full path for the input shapefile
            input_shapefile = os.path.join(input_folder, filename)
            
            # Generate output shapefile filename by adding "_index.shp" suffix
            output_shapefile = os.path.join(output_folder, filename.replace(".shp", "_index.shp"))

            # Create a new shapefile with the same extent as the input raster
            arcpy.management.CreateFeatureclass(output_folder, os.path.basename(output_shapefile), "POLYGON", spatial_reference=input_raster_for_extent)
            
            # Add a new field called 'seagrass' to the shapefile
            arcpy.AddField_management(output_shapefile, "seagrass", "SHORT")

            # Create a cursor to insert features into the output shapefile
            with arcpy.da.InsertCursor(output_shapefile, ["SHAPE@", "seagrass"]) as cursor:
                # Create a polygon for each extent within the input raster extent
                extent_poly = arcpy.Polygon(arcpy.Array([extent.lowerLeft, 
                                                          arcpy.Point(extent.XMin, extent.YMax), 
                                                          extent.upperRight, 
                                                          arcpy.Point(extent.XMax, extent.YMin)]))
                cursor.insertRow([extent_poly, 0])  # Insert polygon with 'seagrass' field as 0 for entire extent

                # Open the input shapefile
                with arcpy.da.SearchCursor(input_shapefile, ["SHAPE@"]) as cursor_input:
                    for row_input in cursor_input:
                        # Get the extent of the input shapefile feature
                        extent_shapefile = row_input[0].extent

                        # Convert the extents to polygons
                        extent_poly_input = arcpy.Polygon(arcpy.Array([extent_shapefile.lowerLeft, 
                                                                       arcpy.Point(extent_shapefile.XMin, extent_shapefile.YMax), 
                                                                       extent_shapefile.upperRight, 
                                                                       arcpy.Point(extent_shapefile.XMax, extent_shapefile.YMin)]))
                        
                        # If the extent of the input shapefile feature intersects with the extent of the input raster, insert it into the output shapefile
                        if extent_poly.intersect(extent_poly_input, 1).area > 0:
                            cursor.insertRow([row_input[0], 1])  # Insert input shapefile feature with 'seagrass' field as 1

def generate_raster(input_shapefile, output_raster, cell_size, bpp=8):
    # Define the output raster coordinate system (optional, modify as needed)
    sr = arcpy.Describe(input_shapefile).spatialReference

    # Perform Polygon to Raster conversion
    arcpy.conversion.PolygonToRaster(input_shapefile, "Seagrass", "temp_raster", "CELL_CENTER", "NONE", cell_size)

    # Copy the raster to the desired output raster with specified bpp
    arcpy.management.CopyRaster("temp_raster", output_raster, pixel_type="8_BIT_UNSIGNED" if bpp == 8 else
                                "16_BIT_UNSIGNED" if bpp == 16 else "32_BIT_FLOAT")

    # Delete temporary raster
    arcpy.management.Delete("temp_raster")

# Set input and output folder paths
#input_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NC21_Eelgrass_New"
output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021"

input_index_shp = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021\Tool_Temp\merged_shapefile.shp"

# Path to the input raster from which to get cell size
input_raster_for_extent = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NorthCov21_Clipped.tif"

# Get cell size of the input raster
desc = arcpy.Describe(input_raster_for_extent)
cell_size = desc.children[0].meanCellHeight
print('cell size is ', cell_size)

# Create index shapefile
#create_index_shapefile(input_folder, output_folder, input_raster_for_extent)

'''
# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".shp"):
        # Construct full path for the input shapefile
        input_shapefile = os.path.join(input_folder, filename)
        print('input shapefile name is ', input_shapefile)
        
        # Generate output shapefile filename by adding "_copy" suffix
        output_shapefile = os.path.join(output_folder, filename.replace(".shp", "_copy.shp"))

        # Make a copy of the input shapefile
        arcpy.CopyFeatures_management(input_shapefile, output_shapefile)

        # Add a new field called 'seagrass' to the copied shapefile
        arcpy.AddField_management(output_shapefile, "seagrass", "SHORT")

        # Calculate the 'seagrass' field to assign a value of 1 to all records
        arcpy.CalculateField_management(output_shapefile, "seagrass", 1, "PYTHON3")
        
        # Generate output raster filename by replacing ".shp" with ".tif"
        output_raster = os.path.join(output_folder, filename.replace(".shp", ".tif"))

        # Generate raster
        generate_raster(output_shapefile, output_raster, cell_size)
        
        print("***************output index raster created *******************")
        print(output_raster)
'''
 
# Generate output raster filename by replacing ".shp" with ".tif"
output_raster = os.path.join(output_folder, "index_tif.tif")
arcpy.env.workspace = output_folder

# Generate raster
generate_raster(input_index_shp, output_raster, cell_size, bpp=8)

print("***************output index raster created *******************")
print(output_raster) 
        