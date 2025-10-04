# 1. create index tif with same extent and cell size as drone image tif

# Set up python env as ArcGIS python interpreter to utilize ArcPy: C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3

# Create_Index_tif_same_input_extent.py

# pre 2. need to put all tif of one year into the {year} folder (I think there is a script for it.. searching...))

# 2. With drone image tif and index tif ready, clip both tif by a specified size (e.g. 512\*512)

# clip_image_rasterio.py

# 3. Once both drone imagery and index are clipped to tiles, move them from seperate state/year folder to a state/image folder for further use

# copy_all_model_image_to_folder.py

# 3.5. From 8/3/24, use select-index-between-5-90.py

# the index with 5%-90% non-blank pixel coverage are copied to image/State/index, and the corresponding images are copied to image/State/image also.

# 4. Collect processed images/indexes number

# count-png-in-subfolder.py

# 5. Validate processed images/indexes number in image folder

# count-image-counts.py
