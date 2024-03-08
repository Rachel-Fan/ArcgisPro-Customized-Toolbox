import arcpy
import os

# Set input and output folder paths
input_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NC21_Eelgrass_New"
output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021"

# Path to the input raster from which to get cell size
input_raster_for_cell_size = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NorthCov21_Clipped.tif"

# Get cell size of the input raster
desc = arcpy.Describe(input_raster_for_cell_size)
cell_size = desc.children[0].meanCellHeight
print('cell size is ', cell_size)
#cell_size = desc.meanCellHeight

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

        # Add a new field called 'Eelgrass' to the copied shapefile
        arcpy.AddField_management(output_shapefile, "Eelgrass", "SHORT")

        # Calculate the 'Eelgrass' field to assign a value of 1 to all records
        arcpy.CalculateField_management(output_shapefile, "Eelgrass", 1, "PYTHON3")
        
        # Generate output raster filename by replacing ".shp" with ".tif"
        #output_raster = os.path.join(output_folder, filename.replace(".shp", ".tif"))
        output_raster = os.path.join(output_folder, 'index_raster.tif')

        # Define the output raster coordinate system (optional, modify as needed)
        sr = arcpy.Describe(input_shapefile).spatialReference

        # Perform Polygon to Raster conversion
        arcpy.conversion.PolygonToRaster(output_shapefile, "Eelgrass", output_raster, "CELL_CENTER", "NONE", cell_size)
        
        print("***************output index raster created *******************")
        print(output_raster)
        
        # Delete the output shapefile
        arcpy.Delete_management(output_shapefile)

        # Optional: If you want to assign NoData values to areas outside polygons, uncomment the following lines
        # arcpy.env.extent = arcpy.Describe(input_shapefile).extent
        # arcpy.env.mask = input_shapefile
        # arcpy.gp.RasterCalculator_sa("Con(IsNull(\"output_raster\"), 0, 1)", "final_output_raster.tif")
