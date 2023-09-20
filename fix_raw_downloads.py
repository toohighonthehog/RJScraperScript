#import os, shutil
from module_rjscanfix import *

# need to find a way to deal with 2 parters.  Until then, do them manually.

BASE_DIRECTORY = "/mnt/multimedia/~Downloads/qBitTorrent.filing/"
TARGET_DIRECTORY = "/mnt/multimedia/~Downloads/filing/"
BASE_EXTENSIONS = [".mkv",".mp4",".avi"]

my_logger = get_logger()

scanned_directory = get_list_of_files(TARGET_DIRECTORY, BASE_EXTENSIONS)
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
