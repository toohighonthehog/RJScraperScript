from module_rjscanfix import *

# Define the directory you want to start the search + the file extension + language suffix

# task:
#   0 = process as normal
#   1 =
#   9 = redo

PROCESS_DIRECTORIES = [ \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/General/", 'prate': 0, 'task': 9}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/07/", 'prate': 7, 'task': 9}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/08/", 'prate': 8, 'task': 9}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/09/", 'prate': 9, 'task': 9}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/10/", 'prate': 10, 'task': 9}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Names/", 'prate': 0, 'task': 9}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Series/", 'prate': 0, 'task': 9}]

#PROCESS_DIRECTORIES = [{'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/12/", 'prate': 0}]
#TARGET_DIRECTORY = BASE_DIRECTORY
BASE_EXTENSIONS = [".mkv", ".mp4", ".avi"]
TARGET_LANGUAGE = "en.srt"
#ARBITRARY_PRATE = 0

my_connection = mysql.connector.connect( 
    user="rjohnson", 
    password="5Nf%GB6r10bD", 
    host="diskstation.hachiko.int", 
    port=3306, 
    database="Multimedia" 
)

my_cursor = my_connection.cursor()
my_logger = get_logger()

if __name__ == "__main__":

    for PROCESS_DIRECTORY in PROCESS_DIRECTORIES:
        BASE_DIRECTORY = PROCESS_DIRECTORY['base']
        TARGET_DIRECTORY = BASE_DIRECTORY
        ARBITRARY_PRATE = PROCESS_DIRECTORY['prate']
        PROCESS_TASK = PROCESS_DIRECTORY['task']

        if not os.path.exists(TARGET_DIRECTORY):
            my_logger.critical(TARGET_DIRECTORY + " does not exist.  Terminating.")
            exit()

        
        my_logger.info("===== " + TARGET_DIRECTORY + " " + ("=" * (93 - (len(TARGET_DIRECTORY)))))

        if (PROCESS_TASK == 9):
            scanned_directory = os.listdir(BASE_DIRECTORY)
            for full_filename in scanned_directory:
                if os.path.isdir(BASE_DIRECTORY + full_filename):
                    filename, file_extension = os.path.splitext(os.path.basename(full_filename))
                    move_down_level(f_base_directory = BASE_DIRECTORY, \
                                    f_target_directory = TARGET_DIRECTORY, \
                                    f_process_file = filename, \
                                    f_base_extensions = BASE_EXTENSIONS, \
                                    f_my_logger = my_logger)



        scanned_directory = get_list_of_files(f_base_directory = BASE_DIRECTORY, \
                                            f_base_extensions = BASE_EXTENSIONS)
        # Scan through the folder
        for full_filename in scanned_directory:
            filename, file_extension = os.path.splitext(os.path.basename(full_filename))
            
            file_match_list = search_for_title(filename)
            
            if len(file_match_list) == 1:
                to_be_scraped = (file_match_list[0])
                my_logger.info("+++++ " + filename + file_extension + " +++++ (single match found).")

                subtitle_available = download_subtitlecat(f_target_directory = TARGET_DIRECTORY, \
                    f_target_language = TARGET_LANGUAGE, \
                    f_process_title = to_be_scraped, \
                    f_my_logger = my_logger)

                metadata_array, metadata_url = download_metadata(f_target_directory = TARGET_DIRECTORY, \
                    f_process_title = to_be_scraped, \
                    f_process_extension = file_extension, \
                    f_process_subtitle_available = subtitle_available, \
                    f_process_arbitrary_prate = ARBITRARY_PRATE, \
                    f_my_logger = my_logger )
                
                metadata_array, process_file_name = move_to_directory(f_base_directory = BASE_DIRECTORY, \
                    f_target_directory = TARGET_DIRECTORY, \
                    f_target_language = TARGET_LANGUAGE, \
                    f_process_file = filename, \
                    f_process_extension = file_extension, \
                    f_my_logger = my_logger, \
                    f_metadata_array = metadata_array)
                
                send_data_to_database(f_metadata_array = metadata_array, \
                    f_metadata_url = metadata_url, \
                    f_my_logger = my_logger, \
                    f_my_cursor = my_cursor) ; my_connection.commit()

                send_data_to_json(f_metadata_array = metadata_array, \
                    f_metadata_url = metadata_url, \
                    f_my_logger = my_logger, \
                    f_json_filename = TARGET_DIRECTORY + process_file_name + "/" + process_file_name + ".json")

            else:
                my_logger.warning("+++++ " + filename + file_extension + " +++++ (skipping. " + str(len(search_for_title(filename)) + " results found)."))

            my_logger.info("=" * 100)

    my_cursor.close()
    my_connection.disconnect()




    
