import os
import shutil

# Define the directory you want to start the search in
start_directory = "/path/to/your/directory"

# Define the file extension you want to search for
target_extension = ".txt"

# Maximum depth to search (3 levels deep)
max_depth = 3

# Function to move a file to a folder with the same name as its extension
def move_file_to_extension_folder(file_path):
    _, file_name = os.path.split(file_path)
    extension = os.path.splitext(file_name)[1]
    extension_folder = os.path.join(os.path.dirname(file_path), extension.lstrip('.'))
    
    if not os.path.exists(extension_folder):
        os.makedirs(extension_folder)
    
    destination_path = os.path.join(extension_folder, file_name)
    shutil.move(file_path, destination_path)
    print(f"Moved '{file_name}' to '{extension_folder}'")

# Recursively search and move files
for root, _, files in os.walk(start_directory):
    depth = root.count(os.path.sep) - start_directory.count(os.path.sep)
    if depth > max_depth:
        continue
    
    for file in files:
        if file.endswith(target_extension):
            file_path = os.path.join(root, file)
            move_file_to_extension_folder(file_path)