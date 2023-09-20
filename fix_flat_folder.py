#import sys, os, re, requests, json, logging, time, hashlib
from module_rjscanfix import *
#import mysql.connector
#from requests_html import HTMLSession
#from javscraper import *


# Define the directory you want to start the search + the file extension + language suffix
BASE_DIRECTORY = "/mnt/multimedia/Other/RatedFinalJ/Censored/12/"
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
                move_down_level(BASE_DIRECTORY, TARGET_DIRECTORY, filename, BASE_EXTENSIONS)

    my_logger.info("================================================================================================")

    scanned_directory = get_list_of_files(BASE_DIRECTORY, BASE_EXTENSIONS)
    # Scan through the folder
    for full_filename in scanned_directory:
        #if os.path.isfile(BASE_DIRECTORY + file) and file.lower().endswith(TARGET_EXTENSION):

        filename, file_extension = os.path.splitext(os.path.basename(full_filename))
        if len(search_for_title(filename)) == 1:
            my_logger.info("+++++ " + filename + file_extension + " +++++ (single match found).")
            to_be_scraped = move_to_directory(BASE_DIRECTORY, TARGET_DIRECTORY, TARGET_LANGUAGE, filename, file_extension)
            subtitle_available = download_subtitlecat(TARGET_DIRECTORY, TARGET_LANGUAGE, to_be_scraped)
            download_metadata(TARGET_DIRECTORY, to_be_scraped, file_extension, subtitle_available, ARBITRARY_PRATE)

        else:
            my_logger.warning("+++++ " + filename + file_extension + " +++++ (skipping. " + str(len(search_for_title(filename)) + " results found)."))

        my_logger.info("================================================================================================")

    my_cursor.close()




    
