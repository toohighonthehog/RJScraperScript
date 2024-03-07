#from module_rjscanfix import *
import os, shutil
import rjscanmodule.rjlogging as rjlog
import rjscanmodule.rjgeneral as rjgen

PROCESS = "COPY"
BASE_DIRECTORY = "/home/rjohnson/test/qb.1/"
INTERMEDIATE_DIRECTORY = "/home/rjohnson/test/qb.2/"
TARGET_DIRECTORY = "/home/rjohnson/test/qb.3/"
BASE_EXTENSIONS = [".txt", ".gif"]

if __name__ == "__main__":
    
    my_logger = rjlog.get_logger()

#   stage 1 - move all the useful files to the store
    rjgen.transfer_files_by_extension(f_source_directory=BASE_DIRECTORY,
                                      f_target_directory=INTERMEDIATE_DIRECTORY,
                                      f_extensions=BASE_EXTENSIONS,
                                      f_my_logger=my_logger,
                                      f_processmode=PROCESS)

#   stage 2 - fix all the filenames
#   scanned_directory = rjgen.get_list_of_files(f_source_directory=INTERMEDIATE_DIRECTORY, f_source_extensions=BASE_EXTENSIONS)