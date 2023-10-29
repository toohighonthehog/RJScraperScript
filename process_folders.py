from module_rjscanfix import *
import os
import pathlib
from icecream import ic

# task:
#   0 = Skip - do nothing
#   1 = Just generate the ffmpeg script.
#   2 = Just Scan (right now, only for whisper audio files - can be more)
#   4 = Process files in root of source folder
#   8 = Process Flagged
#  16 = Process missing json.
#  32 = Just undo / reset.  Don't Scan
#  64 = Do DEFAULT_TASK.

# status:
#   1 = rescan
#   5 = create script in Subtitle_Whisper/Audio/runner folder.  # the value should reset when done.

# Subtitles:
#   1 = An export MP3 exists ready for whisper processing. (check)
#
#   9 = Good, local language subtitle found. (check)

os.system('clear')

DEFAULT_TASK = 32 + 4
PROCESS_DIRECTORIES = [
    {'task':   0, 'prate':  0,
        'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/General/"},
    {'task':   0, 'prate':  7, 'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/07/"},
    {'task':   0, 'prate':  8, 'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/08/"},
    {'task':   0, 'prate':  9, 'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/09/"},
    {'task':   2, 'prate': 10, 'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/10/"},
    {'task':   0, 'prate': 12, 'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/12/"},
    {'task':   0, 'prate':  0, 'base': "/mnt/multimedia/Other/RatedFinalJ/Names/"},
    {'task':   0, 'prate':  0, 'base': "/mnt/multimedia/Other/RatedFinalJ/Series/"},
    {'task':   0, 'prate': -1, 'base': "/mnt/multimedia/Other/RatedFinalJ/Request/"}]

SOURCE_EXTENSIONS = [".mkv", ".mp4", ".avi", ".xxx"]
TARGET_LANGUAGE = "en.srt"
SUBTITLE_GENERAL = "/mnt/multimedia/Other/~Miscellaneous/~SubtitleRepository/General/"
SUBTITLE_WHISPER = "/mnt/multimedia/Other/~Miscellaneous/~SubtitleRepository/Whisper/"

BATCH_DATETIME = str(f"{datetime.now():%Y-%m-%d %H:%M:%S}")

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

    # Delete old Subtitle runner.sh file
    pathlib.Path(SUBTITLE_WHISPER + "Audio/runner.sh").unlink(missing_ok=True)

    for PROCESS_DIRECTORY in PROCESS_DIRECTORIES:
        SOURCE_DIRECTORY = PROCESS_DIRECTORY['base']
        TARGET_DIRECTORY = SOURCE_DIRECTORY
        ARBITRARY_PRATE = PROCESS_DIRECTORY['prate']
        PROCESS_TASK = PROCESS_DIRECTORY['task']
        if PROCESS_TASK == 64:
            PROCESS_TASK = DEFAULT_TASK

        if not os.path.exists(SOURCE_DIRECTORY):
            my_logger.critical(SOURCE_DIRECTORY +
                               " does not exist.  Terminating.")
            exit()
        pass

        if not os.path.exists(TARGET_DIRECTORY):
            my_logger.critical(TARGET_DIRECTORY +
                               " does not exist.  Creating.")
            os.makedirs(TARGET_DIRECTORY, exist_ok=True)

        # ic (PROCESS_TASK)

        if (PROCESS_TASK >= 8):
            my_logger.info("===== Source: " + SOURCE_DIRECTORY +
                           " " + ("=" * (85 - (len(SOURCE_DIRECTORY)))))

        # Do pre-scan/process preparations
        # Perform the scan process looking for metadata etc.
        # Revert Everything
        if (PROCESS_TASK & 32):
            my_logger.info(
                "=== Reverting (Mode: Undo Everything )" + ("=" * 62))
            scanned_directory = os.listdir(SOURCE_DIRECTORY)
            for filename in scanned_directory:
                if os.path.isdir(SOURCE_DIRECTORY + filename):
                    pass
                    move_up_level(
                        f_source_directory=SOURCE_DIRECTORY,
                        f_target_directory=TARGET_DIRECTORY,
                        f_process_filename=filename,
                        f_source_extensions=SOURCE_EXTENSIONS,
                        f_my_logger=my_logger)

            my_logger.info("=" * 100)

        # Missing JSON
        if ((PROCESS_TASK & 16) and ~(PROCESS_TASK & 32)):
            records_to_update = get_db_array(my_cursor)
            my_logger.info(
                "=== Reverting (Mode: Missing Metadata )" + ("=" * 61))
            scanned_directory = os.listdir(SOURCE_DIRECTORY)
            for filename in scanned_directory:
                if os.path.isdir(SOURCE_DIRECTORY + filename):
                    pass
                    # (PROCESS_TASK == 1 and (os.path.isfile(SOURCE_DIRECTORY + filename + "/" + filename + ".json") is False) or (filename in records_to_update[0])) or   # 16
                    if (os.path.isfile(SOURCE_DIRECTORY + filename + "/" + filename + ".json") is False):
                        pass
                        move_up_level(
                            f_source_directory=SOURCE_DIRECTORY,
                            f_target_directory=TARGET_DIRECTORY,
                            f_process_filename=filename,
                            f_source_extensions=SOURCE_EXTENSIONS,
                            f_my_logger=my_logger)

            my_logger.info("=" * 100)

        # ic ((PROCESS_TASK & 8))
        # ic (~(PROCESS_TASK & 32))
        # Flagged in Database
        if ((PROCESS_TASK & 8) and ~(PROCESS_TASK & 32)):
            records_to_update = get_db_array(my_cursor)
            # ic (records_to_update)
            my_logger.info("=== Reverting (Mode: Flagged in DB )" + ("=" * 64))
            scanned_directory = os.listdir(SOURCE_DIRECTORY)
            for filename in scanned_directory:
                if os.path.isdir(SOURCE_DIRECTORY + filename):
                    pass
                    if (value_in_list(records_to_update, filename)[1] == 1):
                        pass
                        move_up_level(
                            f_source_directory=SOURCE_DIRECTORY,
                            f_target_directory=TARGET_DIRECTORY,
                            f_process_filename=filename,
                            f_source_extensions=SOURCE_EXTENSIONS,
                            f_my_logger=my_logger)

            my_logger.info("=" * 100)

        # generate ffmpeg script.
        # should we null out the value after running?
        if (PROCESS_TASK & 1):  # 1
            my_logger.info("=== Process Whisper Tags" + "=" * 65)
            my_logger.info("===== Source: " + SOURCE_DIRECTORY +
                           " " + ("=" * (85 - (len(SOURCE_DIRECTORY)))))
            scanned_directory = os.listdir(SOURCE_DIRECTORY)
            records_to_update = get_db_array(my_cursor)
            for filename in scanned_directory:
                # ic (filename)
                # ic (value_in_list(records_to_update, filename))
                pass

                if (value_in_list(records_to_update, filename)[1] == 5):
                    #######################
                    # Do the subtitle thing here if the status attribute is 5.
                    sub_record = (value_in_list(records_to_update, filename))
                    # ic (value_in_list(update_status, title)[1])
                    if ((sub_record[1]) == 5):
                        pass
                        # .replace('/mnt/', '/volume1/')
                        source = (sub_record[2])
                        # .replace('/mnt/', '/volume1/')
                        destination = (SUBTITLE_WHISPER +
                                       "Audio/" + filename + ".mp3")
                        my_logger.info("SUB - Schedule " +
                                       filename + ".mp3 creation in script.")
                        # print ("ffmpeg -i " + source + " " + destination)

                        with open(SUBTITLE_WHISPER + "Audio/runner.sh", 'a') as f:
                            f.write("ffmpeg -i " + source +
                                    " " + destination + "\n")

            my_logger.info("=" * 100)

        # Scan through records and check DB
        if (PROCESS_TASK & 2):  # 2
            my_logger.info("=== Scanning " + "=" * 87)
            my_logger.info("===== Source: " + SOURCE_DIRECTORY +
                           " " + ("=" * (85 - (len(SOURCE_DIRECTORY)))))
            scanned_directory = os.listdir(SOURCE_DIRECTORY)
            for filename in scanned_directory:
                if os.path.isdir(SOURCE_DIRECTORY + filename):
                    db_record = get_db_record(my_cursor, filename)
                    pass
                    if db_record is not None:
                        subtitle_available = (db_record[9])
                        pass
                        if (subtitle_available == 0):
                            if (os.path.isfile(SUBTITLE_WHISPER + "Audio/" + filename + ".mp3")):
                                my_logger.info(
                                    "SUB - Audio Found " + filename + ".mp3 in 'whisper subs'.")
                                # ic (type(db_record))
                                db_record_list = list(db_record)
                                db_record_list[9] = 1
                                db_record = tuple(db_record_list)
                                # ic (db_record[9])
                                put_db_record(my_cursor, db_record)  # 528
                                my_connection.commit()

                        pass
############
############
                        if (subtitle_available <= 8):
                            get_localsubtitles(
                                f_subtitle_general=SUBTITLE_GENERAL,
                                f_subtitle_whisper=SUBTITLE_WHISPER,
                                f_target_directory=TARGET_DIRECTORY,
                                f_target_language=TARGET_LANGUAGE,
                                f_process_title=filename,
                                f_my_logger=my_logger)
                            pass

                            subtitle_available = get_best_subtitle(
                                f_subtitle_whisper=SUBTITLE_WHISPER,
                                f_target_directory=TARGET_DIRECTORY,
                                f_target_language=TARGET_LANGUAGE,
                                f_process_title=filename,
                                f_my_logger=my_logger)
                            pass

                            db_record_list = list(db_record)
                            db_record_list[9] = subtitle_available
                            db_record = tuple(db_record_list)
                            # ic (db_record[9])
                            put_db_record(my_cursor, db_record)  # 528
                            my_connection.commit()

                        pass

        # Do scans and processing.
        if (PROCESS_TASK & 4):  # 4
            my_logger.info("=== Processing " + "=" * 85)
            my_logger.info("===== Source: " + SOURCE_DIRECTORY +
                           " " + ("=" * (85 - (len(SOURCE_DIRECTORY)))))
            my_logger.info("=======> Target: " + TARGET_DIRECTORY +
                           " " + ("=" * (82 - (len(TARGET_DIRECTORY)))))
            scanned_directory = get_list_of_files(
                f_source_directory=SOURCE_DIRECTORY,
                f_source_extensions=SOURCE_EXTENSIONS)

            for full_filename in scanned_directory:
                filename, file_extension = os.path.splitext(
                    os.path.basename(full_filename))
                try:
                    to_be_scraped = (my_javlibrary_new_getvideo(filename)).code
                except:
                    to_be_scraped = ""

                pass

                if to_be_scraped == fix_file_code(filename):
                    my_logger.info("+++++ " + full_filename +
                                   " " + ("+" * (93 - (len(full_filename)))))

                    pass

                    os.makedirs(TARGET_DIRECTORY +
                                fix_file_code(filename), exist_ok=True)

                    get_localsubtitles(
                        f_subtitle_general=SUBTITLE_GENERAL,
                        f_subtitle_whisper=SUBTITLE_WHISPER,
                        f_target_directory=TARGET_DIRECTORY,
                        f_target_language=TARGET_LANGUAGE,
                        f_process_title=to_be_scraped,
                        f_my_logger=my_logger)
                    pass

                    get_subtitlecat(
                        f_target_directory=TARGET_DIRECTORY,
                        f_target_language=TARGET_LANGUAGE,
                        f_process_title=to_be_scraped,
                        f_my_logger=my_logger)

                    pass

                    subtitle_available = get_best_subtitle(
                        f_subtitle_whisper=SUBTITLE_WHISPER,
                        f_target_directory=TARGET_DIRECTORY,
                        f_target_language=TARGET_LANGUAGE,
                        f_process_title=to_be_scraped,
                        f_my_logger=my_logger)

                    pass

                    metadata_array = download_metadata(
                        f_process_title=to_be_scraped,
                        f_subtitle_available=subtitle_available,
                        f_arbitrary_prate=ARBITRARY_PRATE,
                        f_added_date=BATCH_DATETIME,
                        f_my_logger=my_logger)

                    pass

                    metadata_array = move_to_directory(
                        f_source_directory=SOURCE_DIRECTORY,
                        f_target_directory=TARGET_DIRECTORY,
                        f_target_language=TARGET_LANGUAGE,
                        f_process_file=filename,
                        f_process_extension=file_extension,
                        f_my_logger=my_logger,
                        f_metadata_array=metadata_array)

                    pass

                    send_to_database(
                        f_metadata_array=metadata_array,
                        f_my_logger=my_logger,
                        f_my_cursor=my_cursor)
                    my_connection.commit()

                    pass

                    send_to_json(f_metadata_array=metadata_array,
                                 f_my_logger=my_logger,
                                 f_json_filename=TARGET_DIRECTORY + to_be_scraped + "/" + to_be_scraped + ".json")

                else:
                    pattern = r'^[A-Z]{2,5}-\d{3}(?:' + \
                        '|'.join(SOURCE_EXTENSIONS) + ')$'
                    if re.match(pattern, filename + file_extension):

                        my_logger.info("+++++ " + filename + file_extension +
                                       " +++++ no match found but filename is valid.")

                        pass

                        os.makedirs(TARGET_DIRECTORY + filename, exist_ok=True)

                        get_localsubtitles(
                            f_subtitle_general=SUBTITLE_GENERAL,
                            f_subtitle_whisper=SUBTITLE_WHISPER,
                            f_target_directory=TARGET_DIRECTORY,
                            f_target_language=TARGET_LANGUAGE,
                            f_process_title=filename,
                            f_my_logger=my_logger)

                        pass

                        subtitle_available = get_subtitlecat(
                            f_target_directory=TARGET_DIRECTORY,
                            f_target_language=TARGET_LANGUAGE,
                            f_process_title=filename,
                            f_my_logger=my_logger)

                        pass

                        subtitle_available = get_best_subtitle(
                            f_subtitle_whisper=SUBTITLE_WHISPER,
                            f_target_directory=TARGET_DIRECTORY,
                            f_target_language=TARGET_LANGUAGE,
                            f_process_title=filename,
                            f_my_logger=my_logger)

                        # my_logger.info("+++++ " + full_filename + " " + ("+" * (93 - (len(full_filename)))))

                        pass

                        metadata_array = {"code": filename,
                                          "name": None,
                                          "actor": [],
                                          "studio": None,
                                          "image": None,
                                          "genre": [],
                                          "url": [],
                                          "score": None,
                                          "release_date": None,
                                          "added_date": str((f"{datetime.now():%Y-%m-%d %H:%M:%S}")),
                                          "file_date": time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(full_filename))),
                                          "location": TARGET_DIRECTORY + filename + "/" + filename + file_extension,
                                          "subtitles": subtitle_available,
                                          "prate": ARBITRARY_PRATE,
                                          "status": None}

                        pass

                        shutil.move(SOURCE_DIRECTORY + filename + file_extension,
                                    TARGET_DIRECTORY + filename + "/" + filename + file_extension)

                        pass

                        send_to_database(
                            f_metadata_array=metadata_array,
                            f_my_logger=my_logger,
                            f_my_cursor=my_cursor)
                        my_connection.commit()

                    else:

                        my_logger.warning(
                            "+++++ " + filename + file_extension + " +++++ no match found.")
                my_logger.info("=" * 100)

    my_cursor.close()
    my_connection.disconnect()
