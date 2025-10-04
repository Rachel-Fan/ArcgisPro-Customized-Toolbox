import os
import zipfile

def unzip_all_in_folder(input_folder):
    """
    Recursively find all zip files under input_folder and unzip them
    into their containing folder.
    """
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".zip"):
                zip_path = os.path.join(root, file)
                extract_path = root  # extract into the same folder
                try:
                    print(f"📂 Extracting: {zip_path}")
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_path)
                    print(f"✅ Extracted to: {extract_path}")
                except Exception as e:
                    print(f"❌ Failed to extract {zip_path}: {e}")

if __name__ == "__main__":
    input_folder = r"D:\Eelgrass_Classified_from_Metashape\Washington"  # 🔁 change to your folder
    unzip_all_in_folder(input_folder)
