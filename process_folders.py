from module_rjscanfix import *
import os

# task:
#   0 = process as normal / full
#   1 = just process / only new + missing json / [flagged].
#   2 = just process / only new / [flagged]/
#   3 = just process [flagged]
#   8 = scan to make sure files are where they're supposed to be.
#   9 = just undo / reset

os.system('clear')

PROCESS_DIRECTORIES = [ \
                    {'task': 1, 'prate':  0, 'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/General/"}, \
                    {'task': 1, 'prate':  7, 'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/07/"}, \
                    {'task': 1, 'prate':  8, 'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/08/"}, \
                    {'task': 1, 'prate':  9, 'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/09/"}, \
                    {'task': 1, 'prate': 10, 'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/10/"}, \
                    {'task': 1, 'prate':  0, 'base': "/mnt/multimedia/Other/RatedFinalJ/Names/"}, \
                    {'task': 1, 'prate':  0, 'base': "/mnt/multimedia/Other/RatedFinalJ/Series/"}, \
                    {'task': 1, 'prate': -1, 'base': "/mnt/multimedia/Other/RatedFinalJ/Request/"}]

SOURCE_EXTENSIONS = [".mkv", ".mp4", ".avi", ".xxx"]
TARGET_LANGUAGE = "en.srt"
SUBTITLE_GENERAL = "/mnt/multimedia/Other/RatedFinalJ/~SubtitleRepository/General/"
SUBTITLE_WHISPER = "/mnt/multimedia/Other/RatedFinalJ/~SubtitleRepository/Whisper/"
BATCH_DATETIME = str(f"{datetime.now():%Y-%m-%d %H:%M:%S}")

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
            my_logger.info("=== Reverting (Mode:" + str(PROCESS_TASK) + ") " + "=" * 77)
            my_logger.info("===== Source: " + SOURCE_DIRECTORY + " " + ("=" * (85 - (len(SOURCE_DIRECTORY)))))
            scanned_directory = os.listdir(SOURCE_DIRECTORY)
            for filename in scanned_directory:
                pass
                if os.path.isdir(SOURCE_DIRECTORY + filename):
                    if ((PROCESS_TASK == 0 or PROCESS_TASK == 9) or
                        (PROCESS_TASK == 1 and os.path.isfile(SOURCE_DIRECTORY + filename + "/" + filename + ".json") is False)):
                            pass
                            move_up_level( \
                                f_source_directory = SOURCE_DIRECTORY, \
                                f_target_directory = TARGET_DIRECTORY, \
                                f_process_filename = filename, \
                                f_source_extensions = SOURCE_EXTENSIONS, \
                                f_my_logger = my_logger)
            my_logger.info("=" * 100)

        pass

        if (PROCESS_TASK == 0 or PROCESS_TASK == 1 or PROCESS_TASK == 2):
            my_logger.info("=== Processing " + "=" * 85)
            my_logger.info("===== Source: " + SOURCE_DIRECTORY + " " + ("=" * (85 - (len(SOURCE_DIRECTORY)))))
            my_logger.info("=======> Target: " + TARGET_DIRECTORY + " " + ("=" * (82 - (len(TARGET_DIRECTORY)))))
            scanned_directory = get_list_of_files( \
                f_source_directory = SOURCE_DIRECTORY, \
                f_source_extensions = SOURCE_EXTENSIONS)

            for full_filename in scanned_directory:
                filename, file_extension = os.path.splitext(os.path.basename(full_filename))
                try:
                    to_be_scraped = (my_javlibrary_new_getvideo(filename)).code
                except:
                    to_be_scraped = ""

                pass

                if to_be_scraped == fix_file_code(filename):
                    my_logger.info("+++++ " + full_filename + " " + ("+" * (93 - (len(full_filename)))))

                    pass

                    os.makedirs(TARGET_DIRECTORY + fix_file_code(filename), exist_ok=True)
        
                    get_localsubtitles( \
                        f_subtitle_general = SUBTITLE_GENERAL, \
                        f_subtitle_whisper = SUBTITLE_WHISPER, \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_process_title = to_be_scraped, \
                        f_my_logger = my_logger)

                    pass

                    get_subtitlecat( \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_target_language = TARGET_LANGUAGE, \
                        f_process_title = to_be_scraped, \
                        f_my_logger = my_logger)
                    
                    pass

                    subtitle_available = get_best_subtitle( \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_target_language = TARGET_LANGUAGE, \
                        f_process_title = to_be_scraped, \
                        f_my_logger = my_logger)
                    
                    pass
                    
                    metadata_array = download_metadata( \
                        f_process_title = to_be_scraped, \
                        f_subtitle_available = subtitle_available, \
                        f_arbitrary_prate = ARBITRARY_PRATE, \
                        f_added_date = BATCH_DATETIME, \
                        f_my_logger = my_logger)
                                                                    
                    pass

                    metadata_array = move_to_directory( \
                        f_source_directory = SOURCE_DIRECTORY, \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_target_language = TARGET_LANGUAGE, \
                        f_process_file = filename, \
                        f_process_extension = file_extension, \
                        f_my_logger = my_logger, \
                        f_metadata_array = metadata_array)

                    pass

                    send_to_database( \
                        f_metadata_array = metadata_array, \
                        f_my_logger = my_logger, \
                        f_my_cursor = my_cursor) ; my_connection.commit()

                    pass

                    send_to_json(f_metadata_array = metadata_array, \
                        f_my_logger = my_logger, \
                        f_json_filename = TARGET_DIRECTORY + to_be_scraped + "/" + to_be_scraped + ".json")

                else:
                    pattern = r'^[A-Z]{2,5}-\d{3}(?:' + '|'.join(SOURCE_EXTENSIONS) + ')$'
                    if re.match(pattern, filename + file_extension):
                        
                        my_logger.info("+++++ " + filename + file_extension + " +++++ no match found but filename is valid.")
                        
                        pass

                        os.makedirs(TARGET_DIRECTORY + filename, exist_ok=True)

                        get_localsubtitles( \
                        f_subtitle_general = SUBTITLE_GENERAL, \
                        f_subtitle_whisper = SUBTITLE_WHISPER, \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_process_title = filename, \
                        f_my_logger = my_logger)

                        pass

                        subtitle_available = get_subtitlecat( \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_target_language = TARGET_LANGUAGE, \
                        f_process_title = filename, \
                        f_my_logger = my_logger)

                        pass

                        subtitle_available = get_best_subtitle( \
                        f_target_directory = TARGET_DIRECTORY, \
                        f_target_language = TARGET_LANGUAGE, \
                        f_process_title = filename, \
                        f_my_logger = my_logger)

                        # my_logger.info("+++++ " + full_filename + " " + ("+" * (93 - (len(full_filename)))))

                        pass

                        metadata_array = {"code": filename, \
                            "name": None, \
                            "actor": [], \
                            "studio": None, \
                            "image": None, \
                            "genre": [], \
                            "url" : [], \
                            "score": None, \
                            "release_date": None, \
                            "added_date": str((f"{datetime.now():%Y-%m-%d %H:%M:%S}")), \
                            "file_date": time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(full_filename))), \
                            "location": TARGET_DIRECTORY + filename + "/" + filename + file_extension, \
                            "subtitles": subtitle_available, \
                            "prate": ARBITRARY_PRATE}

                        pass

                        shutil.move (SOURCE_DIRECTORY + filename + file_extension, TARGET_DIRECTORY + filename + "/" + filename + file_extension)

                        pass

                        send_to_database( \
                            f_metadata_array = metadata_array, \
                            f_my_logger = my_logger, \
                            f_my_cursor = my_cursor) ; my_connection.commit()

                    else:
                    
                        my_logger.warning("+++++ " + filename + file_extension + " +++++ no match found.")
                my_logger.info("=" * 100)

    my_cursor.close()
    my_connection.disconnect()
