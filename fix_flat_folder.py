from module_rjscanfix import *
from os import system

# task:
#   0 = process as normal
#   1 = just process
#     = skip
#   9 = just undo

system('clear')

PROCESS_DIRECTORIES = [ \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/General/", 'prate': 0, 'task': 2}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/07/", 'prate': 7, 'task': 2}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/08/", 'prate': 8, 'task': 0}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/09/", 'prate': 9, 'task': 1}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/10/", 'prate': 10, 'task': 0}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/12/", 'prate': 12, 'task': 2}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Names/", 'prate': 0, 'task': 2}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Series/", 'prate': 0, 'task': 2}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Request/", 'prate': -1, 'task': 2}]

#PROCESS_DIRECTORIES = [{'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/12/", 'prate': 0}]

SOURCE_EXTENSIONS = [".mkv", ".mp4", ".avi", ".xxx"]
TARGET_LANGUAGE = "en.srt"
SUBTITLE_REPOSITORY = "/mnt/multimedia/Other/X/SRT Files Project/3. Fixed Subs/"

my_connection = mysql.connector.connect( 
    user="rjohnson", 
    password="5Nf%GB6r10bD", 
    host="diskstation.hachiko.int", 
    port=3306, 
    database="Multimedia_Dev" 
)

my_cursor = my_connection.cursor()
my_logger = get_logger()

if __name__ == "__main__":

    for PROCESS_DIRECTORY in PROCESS_DIRECTORIES:
        SOURCE_DIRECTORY = PROCESS_DIRECTORY['base']
        TARGET_DIRECTORY = SOURCE_DIRECTORY
        ARBITRARY_PRATE = PROCESS_DIRECTORY['prate']
        PROCESS_TASK = PROCESS_DIRECTORY['task']

        if not os.path.exists(SOURCE_DIRECTORY):
            my_logger.critical(SOURCE_DIRECTORY + " does not exist.  Terminating.")
            exit()

        pass

        if not os.path.exists(TARGET_DIRECTORY):
            my_logger.critical(TARGET_DIRECTORY + " does not exist.  Creating.")
            os.makedirs(TARGET_DIRECTORY, exist_ok=True)
            exit()

        pass

        if (PROCESS_TASK == 0 or PROCESS_TASK == 1 or PROCESS_TASK == 9):
            my_logger.info("===== Source: " + SOURCE_DIRECTORY + " " + ("=" * (85 - (len(SOURCE_DIRECTORY)))))
            my_logger.info("=======> Target: " + TARGET_DIRECTORY + " " + ("=" * (82 - (len(TARGET_DIRECTORY)))))

        if (PROCESS_TASK == 0 or PROCESS_TASK == 9):
            scanned_directory = os.listdir(SOURCE_DIRECTORY)
            for full_filename in scanned_directory:
                if os.path.isdir(SOURCE_DIRECTORY + full_filename):
                    filename, file_extension = os.path.splitext(os.path.basename(full_filename))
                    move_up_level( \
                        f_source_directory = SOURCE_DIRECTORY, \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_process_filename = filename, \
                        f_source_extensions = SOURCE_EXTENSIONS, \
                        f_my_logger = my_logger)
            my_logger.info("=" * 100)

        pass

        if (PROCESS_TASK == 0 or PROCESS_TASK == 1):
            scanned_directory = get_list_of_files( \
                f_source_directory = SOURCE_DIRECTORY, \
                f_source_extensions = SOURCE_EXTENSIONS)

            for full_filename in scanned_directory:
                filename, file_extension = os.path.splitext(os.path.basename(full_filename))
                #file_match_list = search_for_title(filename)
                try:
                    to_be_scraped = (my_javlibrary_new_getvideo(filename)).code
                except:
                    to_be_scraped = ""

                pass

                if to_be_scraped == fix_file_code(filename):
                    subtitle_available = 0
                    #to_be_scraped = fix_file_code(filename)
                    my_logger.info("+++++ " + full_filename + " +++++ (single match found).")

                    pass
                    os.makedirs(TARGET_DIRECTORY + fix_file_code(filename), exist_ok=True)
        
                    subtitle_available = get_localsubtitle( \
                        f_subtitle_repository = SUBTITLE_REPOSITORY, \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_process_title = to_be_scraped, \
                        f_subtitle_available = subtitle_available, \
                        f_my_logger = my_logger)

                    pass

                    subtitle_available = download_subtitlecat( \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_target_language = TARGET_LANGUAGE, \
                        f_process_title = to_be_scraped, \
                        f_subtitle_available = subtitle_available, \
                        f_my_logger = my_logger)
                    
                    pass

                    subtitle_available = get_best_subtitle( \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_target_language = TARGET_LANGUAGE, \
                        f_process_title = to_be_scraped, \
                        f_subtitle_available = subtitle_available, \
                        f_my_logger = my_logger)
                    
                    pass
                    
                    metadata_array = download_metadata( \
                        f_process_title = to_be_scraped, \
                        f_subtitle_available = subtitle_available, \
                        f_arbitrary_prate = ARBITRARY_PRATE, \
                        f_my_logger = my_logger)
                                                                    
                    pass

                    metadata_array, process_file_name = move_to_directory( \
                        f_source_directory = SOURCE_DIRECTORY, \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_target_language = TARGET_LANGUAGE, \
                        f_process_file = filename, \
                        f_process_extension = file_extension, \
                        f_my_logger = my_logger, \
                        f_metadata_array = metadata_array)

                    pass

                    send_data_to_database( \
                        f_metadata_array = metadata_array, \
                        f_my_logger = my_logger, \
                        f_my_cursor = my_cursor) ; my_connection.commit()

                    pass

                    send_data_to_json(f_metadata_array = metadata_array, \
                        f_my_logger = my_logger, \
                        f_json_filename = TARGET_DIRECTORY + process_file_name + "/" + process_file_name + ".json")

                else:
                    my_logger.warning("+++++ " + full_filename + " +++++ no match found.")

                my_logger.info("=" * 100)

    my_cursor.close()
    my_connection.disconnect()




    
