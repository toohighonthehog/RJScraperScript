#import sys, os, re, requests, json, logging, time, hashlib
from module_rjscanfix import *
#import mysql.connector
#from requests_html import HTMLSession
#from javscraper import *

# Define the directory you want to start the search + the file extension + language suffix
BASE_DIRECTORY = "/mnt/multimedia/Other/RatedFinalJ/Censored/General/"
TARGET_DIRECTORY = BASE_DIRECTORY
BASE_EXTENSIONS = [".mkv", ".mp4", ".avi"]
TARGET_LANGUAGE = "en.srt"
ARBITRARY_PRATE = 0
REDO_FILES = True

if __name__ == "__main__":

    my_connection = mysql.connector.connect( 
        user="rjohnson", 
        password="5Nf%GB6r10bD", 
        host="diskstation.hachiko.int", 
        port=3306, 
        database="Multimedia" 
    )

    # where are these used?
    my_cursor = my_connection.cursor()
    my_logger = get_logger()

    if not os.path.exists(TARGET_DIRECTORY):
        my_logger.critical(TARGET_DIRECTORY + " does not exist.  Terminating.")
        exit()

    if REDO_FILES:
        my_logger.info("================================================================================================")
        scanned_directory = os.listdir(BASE_DIRECTORY)
        for full_filename in scanned_directory:
            if os.path.isdir(BASE_DIRECTORY + full_filename):
                filename, file_extension = os.path.splitext(os.path.basename(full_filename))
                move_down_level(f_base_directory = BASE_DIRECTORY, \
                                f_target_directory = TARGET_DIRECTORY, \
                                f_process_file = filename, \
                                f_base_extensions = BASE_EXTENSIONS, \
                                f_my_logger = my_logger)

    my_logger.info("================================================================================================")

    scanned_directory = get_list_of_files(f_base_directory = BASE_DIRECTORY, \
                                          f_base_extensions = BASE_EXTENSIONS)
    # Scan through the folder
    for full_filename in scanned_directory:
        filename, file_extension = os.path.splitext(os.path.basename(full_filename))
        if len(search_for_title(filename)) == 1:
            my_logger.info("+++++ " + filename + file_extension + " +++++ (single match found).")

            to_be_scraped = move_to_directory(f_base_directory = BASE_DIRECTORY, \
                                              f_target_directory = TARGET_DIRECTORY, \
                                              f_target_language = TARGET_LANGUAGE, \
                                              f_process_file = filename, \
                                              f_process_extension = file_extension, \
                                              f_my_logger = my_logger)

            subtitle_available = download_subtitlecat(f_target_directory = TARGET_DIRECTORY, \
                                                      f_target_language = TARGET_LANGUAGE, \
                                                      f_process_title = to_be_scraped, \
                                                      f_my_logger = my_logger)

            metadata_array, metadata_urls = download_metadata(f_target_directory = TARGET_DIRECTORY, \
                                                              f_process_title = to_be_scraped, \
                                                              f_process_extension = file_extension, \
                                                              f_process_subtitle_available = subtitle_available, \
                                                              f_process_arbitrary_prate = ARBITRARY_PRATE, \
                                                              f_my_logger = my_logger )
            
            send_data_to_database(f_metadata_array = metadata_array, \
                                  f_metadata_urls = metadata_urls, \
                                  f_my_logger = my_logger, \
                                  f_my_cursor = my_cursor) ; my_connection.commit()
            
            send_data_to_json(f_metadata_array = metadata_array, \
                              f_metadata_urls = metadata_urls, \
                              f_my_logger = my_logger, \
                              f_json_filename = TARGET_DIRECTORY + to_be_scraped + "/" + to_be_scraped + ".json")

        else:
            my_logger.warning("+++++ " + filename + file_extension + " +++++ (skipping. " + str(len(search_for_title(filename)) + " results found)."))

        my_logger.info("================================================================================================")

    my_cursor.close()
    my_connection.disconnect()




    
