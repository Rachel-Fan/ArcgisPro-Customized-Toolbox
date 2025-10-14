import os
import shutil

# Define a dictionary mapping folder names to state abbreviations
state_mapping = {
    "Alaska": "AK",
    "Bodega Bay": "BB",
    "British Columbia": "BC",
    "Canada": "CA",
    "Oregon": "OR",
    "Washington": "WA"
}

def move_duplicates_to_archive(year_folder_path):
    file_timestamps = {}
    for filename in os.listdir(year_folder_path):
        file_path = os.path.join(year_folder_path, filename)
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(filename)
            if file_extension in file_timestamps:
                existing_timestamp = file_timestamps[file_extension]
                current_timestamp = os.path.getmtime(file_path)
                if current_timestamp < existing_timestamp:
                    archive_folder_path = os.path.join(year_folder_path, 'Archive')
                    os.makedirs(archive_folder_path, exist_ok=True)
                    shutil.move(file_path, archive_folder_path)
                else:
                    file_timestamps[file_extension] = current_timestamp
            else:
                file_timestamps[file_extension] = os.path.getmtime(file_path)


def rename_folders_and_files(input_folder):
    parent_folder_name = os.path.basename(input_folder)
    state_name = state_mapping.get(parent_folder_name, "")

    for study_area in os.listdir(input_folder):
        study_area_path = os.path.join(input_folder, study_area)
        if os.path.isdir(study_area_path):
            # Determine initials for study area
            if '_' in study_area:
                study_area_initials = ''.join(word[0].upper() for word in study_area.split('_'))[:2]
            else:
                study_area_initials = study_area[:2].upper()

            for year_folder in os.listdir(study_area_path):
                year_folder_path = os.path.join(study_area_path, year_folder)
                if os.path.isdir(year_folder_path):
                    # Normalize year folder name (e.g., 19 → 2019)
                    if len(year_folder) == 2:
                        year_folder_new = '20' + year_folder
                        os.rename(year_folder_path, os.path.join(study_area_path, year_folder_new))
                        year_folder = year_folder_new
                    year_folder_path = os.path.join(study_area_path, year_folder)

                    # Handle duplicates
                    move_duplicates_to_archive(year_folder_path)

                    # Ensure Archive folder exists
                    archive_folder_path = os.path.join(year_folder_path, 'Archive')
                    os.makedirs(archive_folder_path, exist_ok=True)

                    # Rename files in folder
                    for filename in os.listdir(year_folder_path):
                        file_path = os.path.join(year_folder_path, filename)
                        if os.path.isfile(file_path):
                            if filename.endswith('.zip'):
                                # Move ZIPs to Archive
                                shutil.move(file_path, archive_folder_path)
                                print(f"Archived: {filename}")
                                continue

                            # Rename normal files
                            year = year_folder[-2:]
                            parts = filename.split('_')
                            new_filename = f"{study_area_initials}_{state_name}_{year}_{parts[-1]}"

                            # 🔧 Replace any double underscores
                            new_filename = new_filename.replace('__', '_')

                            new_path = os.path.join(year_folder_path, new_filename)
                            os.rename(file_path, new_path)
                            print(f"Renamed: {new_filename}")


if __name__ == "__main__":
    print('Rename started...')
    input_folder = r'D:\Eelgrass_Classified_from_Metashape\UTM\BC'  # Update as needed
    rename_folders_and_files(input_folder)
    print('✅ Rename done.')
