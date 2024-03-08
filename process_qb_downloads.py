#from module_rjscanfix import *
import os, shutil
import rjscanmodule.rjlogging as rjlog
import rjscanmodule.rjgeneral as rjgen
#from rjscanmodule import rjlogging as rjlog
#from rjscanmodule import rjgeneral as rjgen

PROCESS = "MOVE"
# BASE_DIRECTORY = "/mnt/multimedia/Other/X/SRT Files Project/1. Raw Subs/"
# INTERMEDIATE_DIRECTORY = "/mnt/multimedia/Other/X/SRT Files Project/2. Dumped Subs/"
# TARGET_DIRECTORY = "/mnt/multimedia/Other/Other/RatedFinalJ/~SubtitleRepository/General/"
# BASE_EXTENSIONS = [".srt"]

BASE_DIRECTORY = "/mnt/vmwareshares/Docker-Download/qBitTorrent.finished/"
INTERMEDIATE_DIRECTORY = "/mnt/vmwareshares/Docker-Download/qBitTorrent.holding/"
TARGET_DIRECTORY = "/mnt/vmwareshares/Docker-Download/qBitTorrent.fixed/"
BASE_EXTENSIONS = [".mkv", ".mp4", ".avi", ".xxx"]

# PROCESS = "COPY"
# BASE_DIRECTORY = "/home/rjohnson/test/qb.1/"
# INTERMEDIATE_DIRECTORY = "/home/rjohnson/test/qb.2/"
# TARGET_DIRECTORY = "/home/rjohnson/test/qb.3/"
# BASE_EXTENSIONS = [".txt", ".gif"]

if __name__ == "__main__":
    my_logger = rjlog.get_logger()

#   stage 1 - move all the useful files to the store
    rjgen.transfer_files_by_extension(f_source_directory=BASE_DIRECTORY,
                                      f_target_directory=INTERMEDIATE_DIRECTORY,
                                      f_extensions=BASE_EXTENSIONS,
                                      f_my_logger=my_logger,
                                      f_processmode=PROCESS)

#   stage 2 - fix all the filenames
    scanned_directory = rjgen.get_list_of_files(f_source_directory=INTERMEDIATE_DIRECTORY, f_source_extensions=BASE_EXTENSIONS)
    
    for full_filename in scanned_directory:
        filename, file_extension = os.path.splitext(os.path.basename(full_filename))
        fixed_filename, fixed_count = rjgen.search_for_title(filename)
        #print (f"{fixed_filename} {fixed_count}")

        if fixed_count == 1:
            new_filename = fixed_filename + file_extension
            if (full_filename != new_filename):
                my_logger.info(rjlog.logt(f"{PROCESS[:3]} - {full_filename} becomes {new_filename}."))
    
                if (PROCESS == "MOVE"):
                    shutil.move(full_filename, TARGET_DIRECTORY + new_filename)
    
                if (PROCESS == "COPY"):
                    shutil.copy(full_filename, TARGET_DIRECTORY + new_filename)

        else:
            my_logger.warning(rjlog.logt(f"SKP - {full_filename} (skipping. {str(fixed_count)} results found)."))

    # go to destination
    # iterate each file
    # run the search_for_files function and rename (or display) that.
