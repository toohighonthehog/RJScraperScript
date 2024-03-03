from module_rjscanfix import *
import os
import shutil

PROCESS = "MOVE"

# BASE_DIRECTORY = "/mnt/multimedia/Other/X/SRT Files Project/1. Raw Subs/"
# INTERMEDIATE_DIRECTORY = "/mnt/multimedia/Other/X/SRT Files Project/2. Dumped Subs/"
# TARGET_DIRECTORY = "/mnt/multimedia/Other/Other/RatedFinalJ/~SubtitleRepository/General/"
# BASE_EXTENSIONS = [".srt"]

BASE_DIRECTORY = "/mnt/vmwareshares/Docker-Download/qBitTorrent.finished/"
INTERMEDIATE_DIRECTORY = "/mnt/vmwareshares/Docker-Download/qBitTorrent.holding/"
TARGET_DIRECTORY = "/mnt/vmwareshares/Docker-Download/qBitTorrent.fixed/"
BASE_EXTENSIONS = [".mkv", ".mp4", ".avi", ".xxx"]

# BASE_EXTENSIONS = [".txt"]

if __name__ == "__main__":
    my_logger = get_logger()

# #   stage 1 - move all the useful files to the store
    transfer_files_by_extension(f_source_directory=BASE_DIRECTORY,
                                f_target_directory=INTERMEDIATE_DIRECTORY,
                                f_extensions=BASE_EXTENSIONS,
                                f_my_logger=my_logger,
                                f_processmode=PROCESS)

    # stage 2 - fix all the filenames
    scanned_directory = get_list_of_files(f_source_directory=INTERMEDIATE_DIRECTORY,
                                          f_source_extensions=BASE_EXTENSIONS)
    
    # Scan through the folder
    for full_filename in scanned_directory:
        filename, file_extension = os.path.splitext(os.path.basename(full_filename))
        fixed_filename = search_for_title(full_filename)

        if len(fixed_filename) == 1:
            new_filename = fix_file_code(fixed_filename[0]) + file_extension
            if (full_filename != new_filename):
                my_logger.info(f"{full_filename} becomes {new_filename}.")
    
                if (PROCESS == "MOVE"):
                    # Test this.
                    shutil.move(full_filename, TARGET_DIRECTORY + new_filename)
    
                if (PROCESS == "COPY"):
                    shutil.copy(full_filename, TARGET_DIRECTORY + new_filename)

            else:
                my_logger.info(f"{full_filename} already correct.")
        else:
            my_logger.warning(f"{full_filename} (skipping. {str(len(fixed_filename))} results found).")

    # go to destination
    # iterate each file
    # run the search_for_files function and rename (or display) that.
