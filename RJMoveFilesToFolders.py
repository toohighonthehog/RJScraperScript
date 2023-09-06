import os
import shutil

# Minecraft - 
# Fortnite - 

# Define the directory you want to start the search in
start_directory = "/mnt/multimedia/Other/RatedFinalJ/Censored/10/"

# Define the file extension you want to search for
target_extension = ".txt"

# Iterate through the directory and its subdirectories
for file in os.listdir(start_directory):
    if os.path.isfile(start_directory + file) and file.endswith(target_extension):
        print(f"Moving : {file}")
        # Get the full path of the file
        #print(file + "xx")
        #file_path = os.path.join(root, file)
        # Extract the extension without the dot
        folder_without_dot = file.replace(target_extension,'')
        extension_without_dot = target_extension.strip(".")
        #print(folder_without_dot + "yy")

        # Create a folder with the same name as the extension if it doesn't exist
        destination_directory = start_directory + folder_without_dot

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        # Move the file to the folder

        print(file)
        print(destination_directory)
        os.rename(start_directory + file, destination_directory + "/" + file)
        print(f"Moved '{file}' to '{destination_directory}'")