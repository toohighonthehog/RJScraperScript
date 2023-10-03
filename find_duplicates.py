import os
from collections import defaultdict

def find_duplicate_files(folder_path, min_file_size):
    # Create a dictionary to store files with the same base name
    file_dict = defaultdict(list)

    # Walk through the folder structure
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Get the base file name without the extension
            base_name = os.path.splitext(file_name)[0]
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size >= min_file_size:
                # Add the file to the dictionary using the base name (ignoring extension)
                file_dict[base_name.lower()].append(file_path)

    # Filter out files with only one occurrence (no duplicates)
    duplicate_files = {base_name: paths for base_name, paths in file_dict.items() if len(paths) > 1}

    return duplicate_files

if __name__ == "__main__":
    folder_path = "/mnt/multimedia/Other/RatedFinalJ/"
    min_file_size = 10 * 1024 * 1024  # 10MB
    duplicate_files = find_duplicate_files(folder_path, min_file_size)

    if duplicate_files:
        print("Duplicate files found:")
        for base_name, paths in duplicate_files.items():
            print(f"File Name (ignoring extension): {base_name}")
            for path in paths:
                print(f"  - {path}")
    else:
        print("No duplicate files found.")
