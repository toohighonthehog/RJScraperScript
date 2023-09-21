from module_rjscanfix import *

# need to find a way to deal with 2 parters.  Until then, do them manually.

BASE_DIRECTORY = "/mnt/multimedia/~Downloads/filing/"
TARGET_DIRECTORY = "/mnt/multimedia/~Downloads/fixed/"
BASE_EXTENSIONS = [".mkv",".mp4",".avi"]
#BASE_EXTENSIONS = [".txt"]

my_logger = get_logger()

# stage 1 - move all the useful files to the store
# move_files_by_extension(f_source_dir = BASE_DIRECTORY, \
#                         f_destination_dir = TARGET_DIRECTORY, \
#                         f_extensions = BASE_EXTENSIONS)

# stage 2 - fix all the filenames
scanned_directory = get_list_of_files(f_base_directory = TARGET_DIRECTORY, \
                                      f_base_extensions = BASE_EXTENSIONS)

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
            my_logger.info(full_filename + " already correct.")
    else:
        my_logger.warning(full_filename + " (skipping. " + str(len(fixed_filename)) + " results found).")

# go to destination
# iterate each file
# run the search_for_files function and rename (or display) that.
