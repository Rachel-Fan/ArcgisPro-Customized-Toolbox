import arcpy
import os


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

            # Calculate the extent of the input shapefile
            with arcpy.da.SearchCursor(input_shapefile, ["SHAPE@"]) as cursor:
                for row in cursor:
                    extent_shapefile = row[0].extent
            
            # Create a cursor to insert features into the output shapefile
            with arcpy.da.InsertCursor(output_shapefile, ["SHAPE@", "seagrass"]) as cursor:
                # Create a polygon for each extent within the input raster extent
                extent_poly = arcpy.Polygon(arcpy.Array([extent.lowerLeft, 
                                                          arcpy.Point(extent.XMin, extent.YMax), 
                                                          extent.upperRight, 
                                                          arcpy.Point(extent.XMax, extent.YMin)]))
                cursor.insertRow([extent_poly, 0])  # Insert polygon with 'seagrass' field as 0 for entire extent
                
                # If the input shapefile extent intersects with the input raster extent, insert it into the output shapefile
                if extent.intersects(extent_shapefile):
                    cursor.insertRow([extent_shapefile, 1])  # Insert input shapefile extent with 'seagrass' field as 1

def generate_raster(input_shapefile, output_raster, cell_size):
    # Define the output raster coordinate system (optional, modify as needed)
    sr = arcpy.Describe(input_shapefile).spatialReference

    # Perform Polygon to Raster conversion
    arcpy.conversion.PolygonToRaster(input_shapefile, "seagrass", output_raster, "CELL_CENTER", "NONE", cell_size)

# Set input and output folder paths
input_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NC21_Eelgrass_New"
output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021"

# Path to the input raster from which to get cell size
input_raster_for_extent = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NorthCov21_Clipped.tif"

# Get cell size of the input raster
desc = arcpy.Describe(input_raster_for_extent)
cell_size = desc.children[0].meanCellHeight
print('cell size is ', cell_size)

# Create index shapefile
create_index_shapefile(input_folder, output_folder, input_raster_for_extent)

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
        
        