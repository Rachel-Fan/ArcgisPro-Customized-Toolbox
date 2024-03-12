import arcpy

def perform_raster_calculator(input_raster, output_raster):
    # Set environment settings to ensure extent matching
    arcpy.env.extent = arcpy.Describe(input_raster).extent
    
    # Perform raster calculator operation
    expression = 'Con(IsNull("{}"), 0, 1)'.format(input_raster)
    arcpy.gp.RasterCalculator_sa(expression, output_raster)

def main():
    NorthCov21_Clipped = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NorthCov21_Clipped.tif"
    NC21_Eelgrass_New = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\2019\Washington\temp_NC_19\output_raster.tif"
    output_tif = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\2019\Washington\temp_NC_19\index_raster.tif"

    perform_raster_calculator(NC21_Eelgrass_New, output_tif)

    print('Raster calculator processing completed')

if __name__ == "__main__":
    main()
