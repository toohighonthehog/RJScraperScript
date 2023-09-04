import os
import shutil

# Define the directory you want to start the search in
start_directory = "/path/to/your/directory"

# Define the file extension you want to search for
target_extension = ".txt"

# Iterate through the directory and its subdirectories
for root, _, files in os.walk(start_directory):
    for file in files:
        if file.endswith(target_extension):
            # Get the full path of the file
            file_path = os.path.join(root, file)

            # Extract the extension without the dot
            extension_without_dot = target_extension.strip(".")

            # Create a folder with the same name as the extension if it doesn't exist
            folder_path = os.path.join(root, extension_without_dot)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Move the file to the folder
            destination_path = os.path.join(folder_path, file)
            shutil.move(file_path, destination_path)
            print(f"Moved '{file}' to '{folder_path}'")