import arcpy

NorthCov21_Clipped = r"C:\Users\Rachel\Documents\Seagrass\Dataset\2019\NC_19_Clipped.tif"
NC21_Eelgrass_New = r"C:\Users\Rachel\Documents\Seagrass\Dataset\Script_0312\output_raster.tif"

output_tif = r"C:\Users\Rachel\Documents\Seagrass\Dataset\Script_0312\index.tif"

# Set environment settings to ensure extent matching
arcpy.env.extent = arcpy.Describe(NorthCov21_Clipped).extent

# Perform raster calculator operation
#arcpy.gp.RasterCalculator_sa('Con(IsNull(NC21_Eelgrass_New), 0, 1)', output_tif)

index_raster = NC21_Eelgrass_New
expression = 'Con(IsNull("{}"), 0, 1)'.format(index_raster.replace("\\", "/"))
print('express is', expression)
arcpy.gp.RasterCalculator_sa(expression, output_tif)

print('Raster calculator processing completed')