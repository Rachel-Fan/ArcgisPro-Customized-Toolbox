# Set up ArcPy env

## C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3

# 1. unzip_all.py

## Run unzip_all.py of the region root folder. The script will extracted all files in the folder and its subfolders where zip file locates.

# 2. rename-by-name-convention.py

## This script sanitizes the naming inconsistency for further use.

# 3. reproject-tif-to-utm.py

## GCS-84 can contribute to incorrect index creation. So reproject the initial drone tif to UTM before creating coresponding index tif.

# 4. create_index_tif.py

## create index tif with same extent and cell size as drone image tif, ensure proper path for output folder

# Set to gpuenv conda environment

# 5. clip_image_rasterio.py

## use rasterio instead of opencv or pil, to handle large scale raster tif.

# 6. select-image-less-than-10-black.py

## filter the all black/over 90% black pixel image to clean up the dataset

# 7. copy-same-name-index.py

## copy the matching index with same name as the images filtered in step 6
