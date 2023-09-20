import os, shutil
from mod_rjscanfix import *

# need to find a way to deal with 2 parters.  Until then, do them manually.

BASE_DIRECTORY = "/mnt/multimedia/~Downloads/qBitTorrent.filing/"
TARGET_DIRECTORY = "/mnt/multimedia/~Downloads/filing/"
TARGET_EXENSIONS = [".mkv",".mp4",".avi"]

def move_files_by_extension(function_source_dir, function_destination_dir, function_extensions):
    for root, _, files in os.walk(function_source_dir):
        for file in files:
            if any(file.endswith(ext) for ext in function_extensions):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(function_destination_dir, file)

                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

                # Move the file to the destination directory
                shutil.move(source_file_path, destination_file_path)
                print(f"Moved: {source_file_path} to {destination_file_path}")

# Call the function to perform the file moves
#move_files_by_extension(BASE_DIRECTORY, TARGET_DIRECTORY, TARGET_EXENSIONS)

my_logger = get_logger()

scanned_directory = get_list_of_files(TARGET_DIRECTORY, TARGET_EXTENSIONS)
# Scan through the folder
for full_filename in scanned_directory:
    filename, file_extension = os.path.splitext(os.path.basename(full_filename))
    fixed_filename = search_for_title(full_filename)

    if len(fixed_filename) == 1:
        new_filename = fix_file_code(fixed_filename[0]) + file_extension
        if (full_filename != new_filename):
            my_logger.info(full_filename + " becomes " + new_filename + ".")
            os.rename(TARGET_DIRECTORY + full_filename, TARGET_DIRECTORY + new_filename)

    else:
        my_logger.warning(full_filename + " (skipping. " + str(len(fixed_filename)) + " results found).")

# go to destination
# iterate each file
# run the search_for_files function and rename (or display) that.
