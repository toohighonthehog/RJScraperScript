import os
import shutil
from RJFixIt import *

source_directory = "/path/to/source_directory"
destination_directory = "/path/to/destination_directory"

file_extensions = [".txt"]

def move_files_by_extension(source_dir, dest_dir, extensions):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(dest_dir, file)

                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

                # Move the file to the destination directory
                shutil.move(source_file_path, destination_file_path)
                print(f"Moved: {source_file_path} to {destination_file_path}")

# Call the function to perform the file moves
#move_files_by_extension(source_directory, destination_directory, file_extensions)

title = "DOCP094"

print (my_javlibrary_new_search(title))
