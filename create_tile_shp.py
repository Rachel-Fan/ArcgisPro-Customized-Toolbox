import rasterio
from shapely.geometry import box
import fiona
from fiona.crs import from_epsg
import os

# Load the TIFF file
tif_path = 'path_to_your_tif_file.tif'
with rasterio.open(tif_path) as src:
    # Get the spatial information
    crs = src.crs
    transform = src.transform
    width = src.width
    height = src.height

# Calculate the size of each pixel in the units of the coordinate system
pixel_width = transform[0]
pixel_height = -transform[4]  # Usually negative because the origin is at the top-left corner

# Define the size of the grid cells (polygons) in pixels
cell_size_pixels = 512

# Calculate the number of cells in each dimension
n_cells_x = width // cell_size_pixels
n_cells_y = height // cell_size_pixels

# Create polygons for each cell
polygons = []
for i in range(n_cells_x):
    for j in range(n_cells_y):
        min_x = transform[2] + i * cell_size_pixels * pixel_width
        max_x = min_x + cell_size_pixels * pixel_width
        min_y = transform[5] + j * cell_size_pixels * pixel_height
        max_y = min_y + cell_size_pixels * pixel_height
        polygons.append(box(min_x, min_y, max_x, max_y))

# Define the schema of the shapefile
schema = {
    'geometry': 'Polygon',
    'properties': {},
}

# Save polygons as a shapefile
shapefile_path = 'path_to_output_shapefile.shp'
with fiona.open(shapefile_path, 'w', 'ESRI Shapefile', schema, crs=from_epsg(crs.to_epsg())) as shp:
    for poly in polygons:
        shp.write({'geometry': poly.__geo_interface__, 'properties': {}})
