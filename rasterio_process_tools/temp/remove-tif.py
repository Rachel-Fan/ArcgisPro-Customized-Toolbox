import os
import glob

def delete_tif_files(directory):
    """
    Deletes all .tif files in the specified directory and its subdirectories.

    :param directory: Path to the root directory where .tif files should be deleted.
    """
    # Recursively find all .tif files
    tif_files = glob.glob(os.path.join(directory, "**", "*.tif"), recursive=True)

    for file in tif_files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

if __name__ == "__main__":
    # path = input("Enter the directory path: ").strip()
    path = f""
    
    if os.path.exists(path) and os.path.isdir(path):
        delete_tif_files(path)
        print("Deletion process completed.")
    else:
        print("Invalid directory path. Please enter a valid path.")
