import os

def count_files_with_patterns(folder_path):
    index_count = 0
    image_count = 0
    index_19_count = 0
    index_20_count = 0
    index_21_count = 0
    index_22_count = 0
    
    image_19_count = 0
    image_20_count = 0
    image_21_count = 0
    image_22_count = 0
    
    index_folder_path = os.path.join(folder_path, "index")
    image_folder_path = os.path.join(folder_path, "image")
    
    # Count files and patterns in 'index' folder
    for filename in os.listdir(index_folder_path):
        if os.path.isfile(os.path.join(index_folder_path, filename)):
            index_count += 1
            if "_19" in filename:
                index_19_count += 1
            if "_20" in filename:
                index_20_count += 1
            if "_21" in filename:
                index_21_count += 1
            if "_22" in filename:
                index_22_count += 1
    
    # Count files and patterns in 'image' folder
    for filename in os.listdir(image_folder_path):
        if os.path.isfile(os.path.join(image_folder_path, filename)):
            image_count += 1
            if "_19" in filename:
                image_19_count += 1
            if "_20" in filename:
                image_20_count += 1
            if "_21" in filename:
                image_21_count += 1
            if "_22" in filename:
                image_22_count += 1
    
    return {
        "index_count": index_count,
        "image_count": image_count,
        "index_19_count": index_19_count,
        "index_20_count": index_20_count,
        "index_21_count": index_21_count,
        "index_22_count": index_22_count,
        "image_19_count": image_19_count,
        "image_20_count": image_20_count,
        "image_21_count": image_21_count,
        "image_22_count": image_22_count,
    }

# Example usage:
folder_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Bodega Bay"
counts = count_files_with_patterns(folder_path)
print("Number of files in 'index' folder:", counts["index_count"])
print("Number of files in 'image' folder:", counts["image_count"])
print("Number of '_19' files in 'index' folder:", counts["index_19_count"])
print("Number of '_20' files in 'index' folder:", counts["index_20_count"])
print("Number of '_21' files in 'index' folder:", counts["index_21_count"])
print("Number of '_22' files in 'index' folder:", counts["index_22_count"])
print("Number of '_19' files in 'image' folder:", counts["image_19_count"])
print("Number of '_20' files in 'image' folder:", counts["image_20_count"])
print("Number of '_21' files in 'image' folder:", counts["image_21_count"])
print("Number of '_22' files in 'image' folder:", counts["image_22_count"])


