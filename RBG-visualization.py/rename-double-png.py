import os

def rename_double_png(folder):
    renamed_count = 0
    for filename in os.listdir(folder):
        if filename.endswith(".png.png"):
            old_path = os.path.join(folder, filename)
            new_filename = filename.replace(".png.png", ".png")
            new_path = os.path.join(folder, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_filename}")
            renamed_count += 1
    print(f"\nTotal files renamed: {renamed_count}")

if __name__ == "__main__":
    # Replace with your actual folder path in WSL (you can use relative or absolute path)
    folder_path = r"\\wsl.localhost\Ubuntu\home\geofly\sam-hq\train\pa-sam-ggb\Alaska-2025\visualize-0522"
    rename_double_png(folder_path)
