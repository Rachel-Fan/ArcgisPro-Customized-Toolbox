import os
import shutil

def find_tif_files(root_dir):
    """Recursively find all .tif files in the given directory and subdirectories."""
    tif_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower().endswith(".tif"):
                tif_files.append(os.path.join(dirpath, file))
    return tif_files

def extract_year_from_path(file_path, source_root):
    """Extracts the year from the file's folder structure."""
    relative_path = os.path.relpath(file_path, source_root)  # Get relative path
    path_parts = relative_path.split(os.sep)  # Split path into parts
    
    # Assume year is always a 4-digit number in the path
    for part in path_parts:
        if part.isdigit() and len(part) == 4:  # Checks if it's a 4-digit year
            return part
    return None  # Return None if no year is found

def copy_tif_by_year(source_root, output_root):
    """Copies .tif files from the source directory into the corresponding year folder in the output directory."""
    tif_files = find_tif_files(source_root)

    if not tif_files:
        print("⚠️ No .tif files found.")
        return

    for tif in tif_files:
        year = extract_year_from_path(tif, source_root)

        if year:
            # Define output directory for this year
            year_output_folder = os.path.join(output_root, year)
            os.makedirs(year_output_folder, exist_ok=True)  # Create if missing

            # Define the destination file path
            destination_tif = os.path.join(year_output_folder, os.path.basename(tif))

            # Copy the file
            shutil.copy2(tif, destination_tif)
            print(f"✅ Copied: {tif} → {destination_tif}")
        else:
            print(f"⚠️ Skipping {tif} (Year not found in path).")

def main():
    source_directory = r"D:\Eelgrass_Classified_from_Metashape\UTM\Alaska"  # Change as needed
    output_directory = r"D:\Eelgrass_Classified_from_Metashape\UTM\DroneImageByYear"  # Change as needed

    print("\n🚀 Copying TIFF files by Year...")
    copy_tif_by_year(source_directory, output_directory)
    print("\n✅ Copying Completed!")

if __name__ == "__main__":
    main()
