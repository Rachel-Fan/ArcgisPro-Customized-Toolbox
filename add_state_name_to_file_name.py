import os
import re

def rename_files(directory):
    # Define the regex pattern to match the filenames
    pattern = re.compile(r'^([A-Z]{2})_(\d{2})_(.*)$')
    
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Check if the filename matches the pattern
            match = pattern.match(filename)
            if match:
                # Construct the new filename
                new_name = f"{match.group(1)}_WA_{match.group(2)}_{match.group(3)}"
                # Get the full paths for the old and new filenames
                old_file = os.path.join(root, filename)
                new_file = os.path.join(root, new_name)
                # Rename the file
                os.rename(old_file, new_file)
                print(f"Renamed '{old_file}' to '{new_file}'")

# Specify the directory to scan and rename files
directory_path = r'C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove'
rename_files(directory_path)
