import os
import shutil

# Define a dictionary mapping folder names to state abbreviations
state_mapping = {
    "Alaska": "AK",
    "Bodega Bay": "BB",
    "Canada": "CA",
    "Oregon": "OR",
    "Washington": "WA"
}

def move_duplicates_to_archive(year_folder_path):
    # Dictionary to store modification timestamps of files with the same extension
    file_timestamps = {}
    for filename in os.listdir(year_folder_path):
        file_path = os.path.join(year_folder_path, filename)
        if os.path.isfile(file_path):
            # Get the file extension
            _, file_extension = os.path.splitext(filename)
            # If the file has the same extension as another file, compare timestamps
            if file_extension in file_timestamps:
                existing_timestamp = file_timestamps[file_extension]
                current_timestamp = os.path.getmtime(file_path)
                # If the current file is older, move it to 'Archive' folder
                if current_timestamp < existing_timestamp:
                    archive_folder_path = os.path.join(year_folder_path, 'Archive')
                    if not os.path.exists(archive_folder_path):
                        os.makedirs(archive_folder_path)
                    shutil.move(file_path, archive_folder_path)
                # If the current file is newer, update the timestamp
                else:
                    file_timestamps[file_extension] = current_timestamp
            # If it's the first file with this extension, add it to the dictionary
            else:
                file_timestamps[file_extension] = os.path.getmtime(file_path)

def rename_folders_and_files(input_folder):
    # Get the parent folder name of the input folder as the state name
    parent_folder_name = os.path.basename(input_folder)
    state_name = state_mapping.get(parent_folder_name, "")

    for study_area in os.listdir(input_folder):
        study_area_path = os.path.join(input_folder, study_area)
        if os.path.isdir(study_area_path):
            # Determine if the study area consists of one word or two words
            if '_' in study_area:
                # If the study area consists of two words, extract initials accordingly
                study_area_initials = ''.join(word[0].upper() for word in study_area.split('_'))[:2]
            else:
                # If the study area consists of one word, take the first two letters
                study_area_initials = study_area[:2].upper()

            for year_folder in os.listdir(study_area_path):
                year_folder_path = os.path.join(study_area_path, year_folder)
                if os.path.isdir(year_folder_path):
                    # Rename year folder to 4-digit format if needed
                    if len(year_folder) == 2:
                        year_folder_new = '20' + year_folder
                        os.rename(year_folder_path, os.path.join(study_area_path, year_folder_new))
                    # Get the updated year folder path
                    year_folder_path = os.path.join(study_area_path, year_folder_new if len(year_folder) == 2 else year_folder)
                    # Move duplicates to 'Archive' folder
                    move_duplicates_to_archive(year_folder_path)
                    # Create 'Archive' folder if it doesn't exist
                    archive_folder_path = os.path.join(year_folder_path, 'Archive')
                    if not os.path.exists(archive_folder_path):
                        os.makedirs(archive_folder_path)
                    # Rename files within the year folder
                    for filename in os.listdir(year_folder_path):
                        file_path = os.path.join(year_folder_path, filename)
                        if os.path.isfile(file_path) and not filename.endswith('.zip'):
                            # Extract year
                            year = year_folder[-2:]
                            # Rename file with state name and study area initials
                            parts = filename.split('_')
                            new_filename = f"{study_area_initials}_{state_name}_{year}_{parts[-1]}"
                            os.rename(file_path, os.path.join(year_folder_path, new_filename))
                            print(new_filename, 'is renamed')
                        elif os.path.isfile(file_path) and filename.endswith('.zip'):
                            # Move .zip files to 'Archive' folder
                            shutil.move(file_path, archive_folder_path)
                            print(file_path, 'is archived')
                       

if __name__ == "__main__":
    print('Rename started')
    input_folder = r'E:\Eelgrass_Classified_from_Metashape\BB_Xiangyu_Shp_GR'  # Replace with the actual path to your input folder
    
    rename_folders_and_files(input_folder)
    print('Rename done')
