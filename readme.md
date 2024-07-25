# 1. create index tif with same extent and cell size as drone image tif

# Create_Index_tif_same_input_extent.py

# 2. With drone image tif and index tif ready, clip both tif by a specified size (e.g. 512\*512)

# clip_image.py

# 3. Once both drone imagery and index are clipped to tiles, move them from seperate state/year folder to a state/image folder for further use

# copy_all_model_image_to_folder.py
