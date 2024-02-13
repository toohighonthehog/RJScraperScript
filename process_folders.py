from module_rjscanfix import *
import os
import pathlib
from icecream import ic
from javscraper import *

# task:
#   0 = Do nothing
#   1 = Generate the ffmpeg script, processed flagged
#   2 = Rescan for subtitles
#   4 = Process files in root of source folder
#   8 = ** Nothing yet **
#  16 = ** Nothing yet **
#  32 = Just undo / reset.  Don't Scan
#  64 = Do DEFAULT_TASK.

#  1, 2 & 8 should be combined as they all just cover rescans initiated from the database. (and run first?)

# status:
#   1 = set for rescan (i.e. already reverted  to parent folder)
#   2 = set for rescan (i.e. revert to parent folder)
#   7 = metadata not found, file not found - wanted.
#   8 = metadata not found, file found.
#   9 = all good.


# Subtitles:
#   1 = ???
#   2 = Trigger for the creation of runner.sh for MP3
#   3 = runner.sh created.
#   4 = The MP3 was created. (do we ever really know this in the usual workflow?)
#   7 = Untranslated Subtitle
#   8 = Untranslated Whisper Subtitles
#   9 = Good, local language subtitle found. (check)

os.system("clear")

DEFAULT_TASK = 1
PROCESS_DIRECTORIES = [
    {"task": 64, "prate": 0, "base": "/multimedia/Other/RatedFinalJ/Censored/General/"},
    {"task": 64, "prate": 7, "base": "/multimedia/Other/RatedFinalJ/Censored/07/"},
    {"task": 64, "prate": 8, "base": "/multimedia/Other/RatedFinalJ/Censored/08/"},
    {"task": 64, "prate": 9, "base": "/multimedia/Other/RatedFinalJ/Censored/09/"},
    {"task": 64, "prate": 10, "base": "/multimedia/Other/RatedFinalJ/Censored/10/"},
    {"task": 4, "prate": 12, "base": "/multimedia/Other/RatedFinalJ/Censored/12/"},
    {"task": 64, "prate": 0, "base": "/multimedia/Other/RatedFinalJ/Names/"},
    {"task": 64, "prate": 0, "base": "/multimedia/Other/RatedFinalJ/Series/"},
    {"task": 64, "prate": -1, "base": "/multimedia/Other/RatedFinalJ/Request/"},
    {"task": 64, "prate": 8, "base": "/multimedia/Other/RatedFinalJ/VR/08/"},
    {"task": 64, "prate": 9, "base": "/multimedia/Other/RatedFinalJ/VR/09/"},
    {"task": 64, "prate": 10, "base": "/multimedia/Other/RatedFinalJ/VR/10/"},
    {"task": 64, "prate": 0, "base": "/multimedia/Other/RatedFinalJ/VR/General/"},
    {"task": 64, "prate": 0, "base": "/multimedia/Other/RatedFinalJ/VR/Names/"}
]

SOURCE_EXTENSIONS = [".mkv", ".mp4", ".avi", ".xxx"]
TARGET_LANGUAGE = "en.srt"
LOCAL_MOUNT_PREFIX = "/mnt"
REMOTE_MOUNT_PREFIX = "file://diskstation"
SUBTITLE_GENERAL = "/mnt/multimedia/Other/~Miscellaneous/~SubtitleRepository/General/"
SUBTITLE_WHISPER = "/mnt/multimedia/Other/~Miscellaneous/~SubtitleRepository/Whisper/"

BATCH_DATETIME = str(f"{datetime.now():%Y-%m-%d %H:%M:%S}")

my_connection = mysql.connector.connect(
    user="rjohnson",
    password="5Nf%GB6r10bD",
    host="diskstation.hachiko.int",
    port=3306,
    database="Multimedia_Dev",
)

my_cursor = my_connection.cursor(dictionary=True)
my_logger = get_logger()

if __name__ == "__main__":
    #pathlib.Path(SUBTITLE_WHISPER + "Audio/runner.sh").unlink(missing_ok=True)

    for PROCESS_DIRECTORY in PROCESS_DIRECTORIES:
        SOURCE_DIRECTORY = LOCAL_MOUNT_PREFIX + PROCESS_DIRECTORY["base"]
        SOURCE_DIRECTORY_R = REMOTE_MOUNT_PREFIX + PROCESS_DIRECTORY["base"]
        TARGET_DIRECTORY = SOURCE_DIRECTORY
        ARBITRARY_PRATE = PROCESS_DIRECTORY["prate"]
        PROCESS_TASK = PROCESS_DIRECTORY["task"]
        if PROCESS_TASK == 64:
            PROCESS_TASK = DEFAULT_TASK

        if not os.path.exists(SOURCE_DIRECTORY):
            my_logger.critical(f"{SOURCE_DIRECTORY} does not exist.  Terminating.")
            exit()
        pass

        if not os.path.exists(TARGET_DIRECTORY):
            my_logger.critical(f"{TARGET_DIRECTORY} does not exist.  Creating.")
            os.makedirs(TARGET_DIRECTORY, exist_ok=True)

        # ic (PROCESS_TASK)

        if PROCESS_TASK >= 1:
            my_logger.info(f"===== Source: {SOURCE_DIRECTORY} ".ljust(100, "="))

        # Revert Everything
        if PROCESS_TASK & 32:
            my_logger.info(f"=== Reverting ( Mode: Undo Everything ) ".ljust(100, "="))
            scanned_directory = os.listdir(SOURCE_DIRECTORY)
            for filename in scanned_directory:
                if os.path.isdir(SOURCE_DIRECTORY + filename):
                    pass
                    move_up_level(
                        f_source_directory=SOURCE_DIRECTORY,
                        f_target_directory=TARGET_DIRECTORY,
                        f_process_filename=filename,
                        f_source_extensions=SOURCE_EXTENSIONS,
                        f_my_logger=my_logger,
                    )

            my_logger.info("=" * 100)

        if (PROCESS_TASK & 1) and ~(PROCESS_TASK & 32):
            my_logger.info("=== Process Rescan Requests ".ljust(100, "="))
           
            # anything with status = 2 in database, revert
            db_query = f"WHERE status = 2 AND location LIKE '{SOURCE_DIRECTORY_R}%'"
            records_to_scan = get_db_array(my_cursor, db_query)

            for record_to_scan in records_to_scan:

                pass
                my_logger.info("=== Reverting ( Mode: Flagged in DB ) ".ljust(100, "="))

                move_up_level(
                    f_source_directory = SOURCE_DIRECTORY,
                    f_target_directory = TARGET_DIRECTORY,
                    f_process_filename = record_to_scan['code'],
                    f_source_extensions = SOURCE_EXTENSIONS,
                    f_my_logger = my_logger,
                    )
                record_to_scan['status'] = 1
                update_db_title_record(my_cursor, record_to_scan)
                my_connection.commit()

            my_logger.info("=== Process MP3 Runner Requests ".ljust(100, "="))

            # anything with subtitles = 2, add to runner.sh MP3 creator then set to 3.
            db_query = f"WHERE subtitles = 2 AND location LIKE '{SOURCE_DIRECTORY_R}%'"
            records_to_scan = get_db_array(my_cursor, db_query)
            
            for record_to_scan in records_to_scan:
                my_logger.info(f"SUB - Add {record_to_scan['code']} to MP3 creation script.")
                source = record_to_scan['location'].replace(REMOTE_MOUNT_PREFIX, LOCAL_MOUNT_PREFIX)
                destination = f"{SUBTITLE_WHISPER}Audio/{record_to_scan['code']}.mp3"
                #destination = destination.replace('/mnt/', '/volume1/')
                with open(SUBTITLE_WHISPER + "Audio/runner.sh", "a") as f:
                    f.write(f"ffmpeg -i {source} {destination}\n")
                record_to_scan['subtitles'] = 3
                update_db_title_record(my_cursor, record_to_scan)
                my_connection.commit()         
            
        if PROCESS_TASK & 2:
            my_logger.info("=== Scanning Subtitles ".ljust(100, "="))

            db_query = f"WHERE subtitles IN (0,1,3,4,5,6,7,8) AND location LIKE '{SOURCE_DIRECTORY_R}%'"
            records_to_scan = get_db_array(my_cursor, db_query)

            for record_to_scan in records_to_scan:
                get_localsubtitles(
                    f_subtitle_general=SUBTITLE_GENERAL,
                    f_subtitle_whisper=SUBTITLE_WHISPER,
                    f_target_directory=TARGET_DIRECTORY,
                    f_target_language=TARGET_LANGUAGE,
                    f_process_title=record_to_scan['code'],
                    f_my_logger=my_logger
                    )

                subtitle_available = get_best_subtitle(
                    f_subtitle_whisper=SUBTITLE_WHISPER,
                    f_target_directory=TARGET_DIRECTORY,
                    f_target_language=TARGET_LANGUAGE,
                    f_process_title=record_to_scan['code'],
                    f_my_logger=my_logger
                    )

                if os.path.isfile(f"{SUBTITLE_WHISPER}Audio/{record_to_scan['code']}.mp3"):
                    my_logger.info(f"SUB - Audio Found {record_to_scan['code']}.mp3 in 'whisper subs'.")
                    if subtitle_available < 4:
                        subtitle_available = 4

                # if 'subtitles' is currently 3 (i.e. in the runner process), leave it alone, unless an '-en.srt' is subsequently found.
                if record_to_scan['subtitles'] == 3 and subtitle_available < 9:
                    subtitle_available = 3

                record_to_scan['subtitles'] = subtitle_available
                update_db_title_record(my_cursor, record_to_scan)
                my_connection.commit()

        # Do scans and processing.
        if PROCESS_TASK & 4:  # 4
            my_logger.info(f"=======> Target: {TARGET_DIRECTORY} ".ljust(100, "="))

            scanned_directory = get_list_of_files(
                f_source_directory=SOURCE_DIRECTORY,
                f_source_extensions=SOURCE_EXTENSIONS
            )

            my_javlibrary = JAVLibrary()
            total = len(scanned_directory)
            count = 0
            for full_filename in scanned_directory:
                count += 1
                filename, file_extension = os.path.splitext(os.path.basename(full_filename))
                to_be_scraped, to_be_scraped_count = search_for_title(filename)

                progress = f" {count}/{total}"

                ### unpick the logic here.
                # if to_be_scraped, do subtitles and move
                # if to_be_scraped_count = 0 and to_be_scaped is null, do empty metadata and move
                # if to_be_scraped_count = 1, do metadata and move
                # if to_be_scraped_count > 1 don't move

                if to_be_scraped:
                    my_logger.info(f"+++++ {full_filename} / {progress}")
                    pass
                    os.makedirs(TARGET_DIRECTORY + search_for_title(filename), exist_ok=True)

                    get_localsubtitles(
                        f_subtitle_general=SUBTITLE_GENERAL,
                        f_subtitle_whisper=SUBTITLE_WHISPER,
                        f_target_directory=TARGET_DIRECTORY,
                        f_target_language=TARGET_LANGUAGE,
                        f_process_title=to_be_scraped,
                        f_my_logger=my_logger
                    )

                    get_subtitlecat(
                        f_target_directory=TARGET_DIRECTORY,
                        f_target_language=TARGET_LANGUAGE,
                        f_process_title=to_be_scraped,
                        f_my_logger=my_logger
                    )

                    subtitle_available = get_best_subtitle(
                        f_subtitle_whisper=SUBTITLE_WHISPER,
                        f_target_directory=TARGET_DIRECTORY,
                        f_target_language=TARGET_LANGUAGE,
                        f_process_title=to_be_scraped,
                        f_my_logger=my_logger
                    )

                    metadata_array = download_metadata(
                        f_process_title=to_be_scraped,
                        f_subtitle_available=subtitle_available,
                        f_arbitrary_prate=ARBITRARY_PRATE,
                        f_added_date=BATCH_DATETIME,
                        f_my_logger=my_logger
                    )

                    metadata_array = move_to_directory(
                        f_source_directory=SOURCE_DIRECTORY,
                        f_target_directory=TARGET_DIRECTORY,
                        f_target_language=TARGET_LANGUAGE,
                        f_process_file=filename,
                        f_process_extension=file_extension,
                        f_my_logger=my_logger,
                        f_metadata_array=metadata_array,
                    )

                    send_to_database(
                        f_metadata_array=metadata_array,
                        f_my_logger=my_logger,
                        f_my_cursor=my_cursor
                    )

                    my_connection.commit()

                    send_to_json(
                        f_metadata_array=metadata_array,
                        f_my_logger=my_logger,
                        f_json_filename=f"{TARGET_DIRECTORY}{to_be_scraped}/{to_be_scraped}.json"
                    )

                else:
                    # this bit...
                    pass
                    #pattern = (r"^[A-Z]{2,7}-\d{3}(?:" + "|".join(SOURCE_EXTENSIONS) + ")$")
                    if to_be_scraped_count == 0:
                        
                        my_logger.info(f"+++++ {filename}{file_extension} +++++ no match found but filename is valid.")

                        os.makedirs(TARGET_DIRECTORY + filename, exist_ok=True)

                        get_localsubtitles(
                            f_subtitle_general=SUBTITLE_GENERAL,
                            f_subtitle_whisper=SUBTITLE_WHISPER,
                            f_target_directory=TARGET_DIRECTORY,
                            f_target_language=TARGET_LANGUAGE,
                            f_process_title=filename,
                            f_my_logger=my_logger,
                        )

                        subtitle_available = get_subtitlecat(
                            f_target_directory=TARGET_DIRECTORY,
                            f_target_language=TARGET_LANGUAGE,
                            f_process_title=filename,
                            f_my_logger=my_logger,
                        )

                        subtitle_available = get_best_subtitle(
                            f_subtitle_whisper=SUBTITLE_WHISPER,
                            f_target_directory=TARGET_DIRECTORY,
                            f_target_language=TARGET_LANGUAGE,
                            f_process_title=filename,
                            f_my_logger=my_logger,
                        )

                        if ARBITRARY_PRATE >= 0:
                            metadata_array = {
                                "code": filename,
                                "name": None,
                                "actor": [],
                                "studio": None,
                                "image": None,
                                "genre": [],
                                "url": [],
                                "score": None,
                                "release_date": None,
                                "added_date": str((f"{datetime.now():%Y-%m-%d %H:%M:%S}")),
                                "file_date": time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(full_filename)),),
                                "location": TARGET_DIRECTORY + filename + "/" + filename + file_extension,
                                "subtitles": subtitle_available,
                                "prate": ARBITRARY_PRATE,
                                "notes": None,
                                "status": 8,
                            }
                        else:
                            metadata_array = {
                                "code": filename,
                                "name": None,
                                "actor": [],
                                "studio": None,
                                "image": None,
                                "genre": [],
                                "url": [],
                                "score": None,
                                "release_date": None,
                                "added_date": None,
                                "file_date": None,
                                "location": None,
                                "subtitles": subtitle_available,
                                "prate": ARBITRARY_PRATE,
                                "notes": None,
                                "status": 7,
                            }

                        pass

                        shutil.move(
                            SOURCE_DIRECTORY + filename + file_extension,
                            TARGET_DIRECTORY + filename + "/" + filename + file_extension
                        )

                        pass

                        send_to_database(
                            f_metadata_array=metadata_array,
                            f_my_logger=my_logger,
                            f_my_cursor=my_cursor
                        )
                        my_connection.commit()

                    else:
                        my_logger.warning(f"+++++ {filename}{file_extension} - no match found ")
                my_logger.info("=" * 100)

    my_cursor.close()
    my_connection.disconnect()
