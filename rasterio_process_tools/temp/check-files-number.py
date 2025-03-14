import os
from collections import defaultdict

def count_files_by_extension(directory):
    """
    Recursively lists the folder structure and counts the number of files per extension in each subfolder.

    :param directory: Path to the root directory to analyze.
    """
    folder_stats = {}

    for root, _, files in os.walk(directory):
        file_counts = defaultdict(int)

        for file in files:
            ext = os.path.splitext(file)[1].lower()  # Get file extension
            file_counts[ext] += 1

        folder_stats[root] = dict(file_counts)  # Convert defaultdict to dict

    return folder_stats

if __name__ == "__main__":
    # path = input("Enter the directory path: ").strip()
    path = r"D:\Eelgrass_processed_images_2025\ModelData\Data\Alaska"

    if os.path.exists(path) and os.path.isdir(path):
        folder_data = count_files_by_extension(path)

        for folder, counts in folder_data.items():
            print(f"\nFolder: {folder}")
            for ext, count in counts.items():
                print(f"  {ext if ext else '[No Extension]'}: {count} files")

        print("\nAnalysis completed.")
    else:
        print("Invalid directory path. Please enter a valid path.")
