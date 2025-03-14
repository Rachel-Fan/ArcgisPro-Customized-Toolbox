# Set up ArcPy env

## C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3

# 1. reproject-tif-to-utem.py

## GCS-84 can contribute to incorrect index creation. So reproject the initial drone tif to UTM before creating coresponding index tif.

# 2. create_index_tif.py

## create index tif with same extent and cell size as drone image tif

# Set to gpuenv conda environment

# 3. copy-image-to-dronebyyear.py

## drone images are need to be under /DroneImageByYear/{State}/{year}

# 4. clip_image_rasterio.py

## use rasterio instead of opencv or pil, to handle large scale raster tif.
