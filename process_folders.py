import javscraper
import rjscanmodule.rjdatabase as rjdb
import rjscanmodule.rjlogging as rjlog
import rjscanmodule.rjgeneral as rjgen
import rjscanmodule.rjmetadata as rjmeta
import rjscanmodule.rjsubtitles as rjsub
import os, shutil, mysql.connector, time

from datetime import datetime

# Task:
#   0 = Do nothing
#   1 = Generate the ffmpeg script, processed flagged
#   2 = Rescan for subtitles
#   4 = Process files in root of source folder
#   8 = Process files in root of source folder (but no SubtitleCat)
#  16 = Write key data to extended attributes
#  32 = Move to folder matching prate
#  64 = Just undo / reset.  Don't Scan
#  128 = Do DEFAULT_TASK.
#  Add some logic on what can be run concurrently.
#  valid values = 1,2,3,4,16,32,36,40,64,68 + 5,9

# are 5 and 9 a reasonable options too?  Do they happen in the right order?

# Status:
#   1 = set for rescan (i.e. already reverted to parent folder)
#   2 = set for rescan (i.e. revert to parent folder)
#   6 = metadata not found, file not found - wanted.
#   7 = metadata found, file not found - wanted.
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

DEFAULT_TASK = 0
PROCESS_DIRECTORIES = [
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/Censored/General/"},
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/Censored/07/"},
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/Censored/08/"},
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/Censored/09/"},
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/Censored/10/"},
    {"task": 128, "prate": -1, "base": "/multimedia/Other/RatedFinalJ/Censored/12/"},
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/Names/"},
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/Series/"},
    {"task": 128, "prate": -1, "base": "/multimedia/Other/RatedFinalJ/Request/"},
    {"task": 4, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/VR/08/"},
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/VR/09/"},
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/VR/10/"},
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/VR/General/"},
    {"task": 128, "prate":  0, "base": "/multimedia/Other/RatedFinalJ/VR/Names/"}
]

# check 5 and 9 are okay.
VALID_TASKS = (0, 1, 2, 3, 4, 5, 8, 9, 16, 32, 36, 64, 68, 72)

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
    database="Multimedia"
)

my_cursor = my_connection.cursor(dictionary=True)
my_logger = rjlog.get_logger()

if __name__ == "__main__":

    for PROCESS_DIRECTORY in PROCESS_DIRECTORIES:
        SOURCE_DIRECTORY = LOCAL_MOUNT_PREFIX + PROCESS_DIRECTORY["base"]
        SOURCE_DIRECTORY_R = REMOTE_MOUNT_PREFIX + PROCESS_DIRECTORY["base"]
        TARGET_DIRECTORY = SOURCE_DIRECTORY
        ARBITRARY_PRATE = PROCESS_DIRECTORY["prate"]
        PROCESS_TASK = PROCESS_DIRECTORY["task"]
     
        if PROCESS_TASK == 128:
            PROCESS_TASK = DEFAULT_TASK

        if PROCESS_TASK not in VALID_TASKS:
            my_logger.warning(rjlog.logt(f_left = f"Invalid task for {SOURCE_DIRECTORY} ", f_middle = "=", f_width = -3))
            PROCESS_TASK = 0

        if PROCESS_TASK >= 1:
            my_logger.info(rjlog.logt(f_left = f"=== Source: {SOURCE_DIRECTORY} ", f_middle = "="))
            if not os.path.exists(SOURCE_DIRECTORY):
                my_logger.critical(rjlog.logt(f"{SOURCE_DIRECTORY} does not exist.  Terminating."))
                exit()

            if not os.path.exists(TARGET_DIRECTORY):
                my_logger.critical(rjlog.logt(f"{TARGET_DIRECTORY} does not exist.  Creating."))
                os.makedirs(TARGET_DIRECTORY, exist_ok=True)
                #my_logger.info(rjlog.logt("="))

        if PROCESS_TASK & 64:
            my_logger.info(rjlog.logt(f_left = "=== Reverting ( Mode: Undo Everything ) ", f_middle = "="))
            scanned_directory = os.listdir(SOURCE_DIRECTORY)
            for filename in scanned_directory:
                if os.path.isdir(SOURCE_DIRECTORY + filename):
                    rjgen.move_up_level(
                        f_source_directory=SOURCE_DIRECTORY,
                        f_target_directory=TARGET_DIRECTORY,
                        f_process_filename=filename,
                        f_source_extensions=SOURCE_EXTENSIONS,
                        f_my_logger=my_logger,
                    )

        if PROCESS_TASK & 16:
            my_logger.info(rjlog.logt(f_left = "=== Process Extended Attributes ", f_middle = "="))
            db_query = f"WHERE location LIKE '{SOURCE_DIRECTORY_R}%'"
            records_to_scan = rjdb.get_db_array(my_cursor, db_query)

            for record_to_scan in records_to_scan:
                code = record_to_scan['code']
                prate = record_to_scan['prate']
                if (prate > 0):
                    full_filename = (record_to_scan['location']).replace('file://diskstation', '/mnt')
                    try:
                        file_xdata_prate = (os.getxattr(full_filename, 'user.prate')).decode("utf-8")
                    except:
                        file_xdata_prate = None

                    if not file_xdata_prate:
                        try:
                            os.setxattr(full_filename, "user.prate", str(prate).encode())
                            my_logger.info(rjlog.logt(f"ATT - Set xattr for {code} to {prate}."))
                        except:
                            my_logger.warning(rjlog.logt(f"ATT - Set xattr for {code} to {prate} failed."))

        if PROCESS_TASK & 32:
            my_logger.info(rjlog.logt(f_left = "=== Move to relevant prate folder ", f_middle = "="))
            db_query = f"WHERE location LIKE '{SOURCE_DIRECTORY_R}%'"
            records_to_scan = rjdb.get_db_array(my_cursor, db_query)

            for record_to_scan in records_to_scan:
                code = record_to_scan['code']
                prate = record_to_scan['prate']
                prate_int = prate
                destination = rjgen.prate_directory(SOURCE_DIRECTORY, prate)
                if (destination):
                    my_logger.info(rjlog.logt(f"{destination} - {code} - {prate}."))
                    try:
                        print (f"{SOURCE_DIRECTORY}{code} > {destination}{code}")
                        shutil.move(SOURCE_DIRECTORY + code, destination + code)
                    except:
                        pass
                    for ext in SOURCE_EXTENSIONS:
                        try:
                            print (f"{destination}{code}/{code}{ext} > {destination}{code}{ext}")
                            shutil.move(destination + code + "/" + code + ext, destination + code + ext)
                        except:
                            pass
                    # shutil.move(SOURCE_DIRECTORY + code, destination + FILE)
                    # move the whole folder to the new target
                    # revert the specific media file (from location) to parent.

        if PROCESS_TASK & 1:
            my_logger.info(rjlog.logt(f_left = "=== Process Rescan Requests ", f_middle = "="))
           
            db_query = f"WHERE status = 2 AND location LIKE '{SOURCE_DIRECTORY_R}%'"
            records_to_scan = rjdb.get_db_array(my_cursor, db_query)

            my_logger.info(rjlog.logt(f_left = "=== Reverting ( Mode: Flagged in DB ) ", f_middle = "="))

            for record_to_scan in records_to_scan:
                rjgen.move_up_level(
                    f_source_directory = SOURCE_DIRECTORY,
                    f_target_directory = TARGET_DIRECTORY,
                    f_process_filename = record_to_scan['code'],
                    f_source_extensions = SOURCE_EXTENSIONS,
                    f_my_logger = my_logger,
                    )
                record_to_scan['status'] = 1
                rjdb.update_db_title_record(my_cursor, record_to_scan)
                my_connection.commit()

            my_logger.info(rjlog.logt(f_left = "=== Process MP3 Runner Requests ", f_middle = "="))

            # anything with subtitles = 2, add to runner.sh MP3 creator then set to 3.
            db_query = f"WHERE subtitles = 2 AND location LIKE '{SOURCE_DIRECTORY_R}%'"
            records_to_scan = rjdb.get_db_array(my_cursor, db_query)
            
            for record_to_scan in records_to_scan:
                my_logger.info(rjlog.logt(f"SUB - Add {record_to_scan['code']} to MP3 creation script."))
                source = record_to_scan['location'].replace(REMOTE_MOUNT_PREFIX, LOCAL_MOUNT_PREFIX)
                destination = f"{SUBTITLE_WHISPER}Audio/{record_to_scan['code']}.mp3"
                #destination = destination.replace('/mnt/', '/volume1/')
                with open(SUBTITLE_WHISPER + "Audio/runner.sh", "a") as f:
                    f.write(f"ffmpeg -i {source} {destination}\n")
                record_to_scan['subtitles'] = 3
                rjdb.update_db_title_record(my_cursor, record_to_scan)
                my_connection.commit()         

        if PROCESS_TASK & 2:
            my_logger.info(rjlog.logt(f_left = "=== Scanning Subtitles ", f_middle = "="))

            db_query = f"WHERE subtitles IN (0,1,3,4,5,6,7,8) AND location LIKE '{SOURCE_DIRECTORY_R}%'"
            records_to_scan = rjdb.get_db_array(my_cursor, db_query)

            for record_to_scan in records_to_scan:
                rjsub.get_localsubtitles(
                    f_subtitle_general=SUBTITLE_GENERAL,
                    f_subtitle_whisper=SUBTITLE_WHISPER,
                    f_target_directory=TARGET_DIRECTORY,
                    f_target_language=TARGET_LANGUAGE,
                    f_process_title=record_to_scan['code'],
                    f_my_logger=my_logger
                    )

                rjsub.get_subtitlecat(
                    f_target_directory=TARGET_DIRECTORY,
                    f_target_language=TARGET_LANGUAGE,
                    f_process_title=record_to_scan['code'],
                    f_my_logger=my_logger
                    )

                subtitle_available = rjsub.get_best_subtitle(
                    f_target_directory=TARGET_DIRECTORY,
                    f_target_language=TARGET_LANGUAGE,
                    f_process_title=record_to_scan['code'],
                    f_my_logger=my_logger
                    )

                if os.path.isfile(f"{SUBTITLE_WHISPER}Audio/{record_to_scan['code']}.mp3"):
                    my_logger.info(rjlog.logt(f"SUB - Audio Found {record_to_scan['code']}.mp3 in 'whisper subs'."))
                    if subtitle_available < 4:
                        subtitle_available = 4

                # if 'subtitles' is currently 3 (i.e. in the runner process), leave it alone, unless an '-en.srt' is subsequently found.
                if record_to_scan['subtitles'] == 3 and subtitle_available < 9:
                    subtitle_available = 3

                record_to_scan['subtitles'] = subtitle_available
                rjdb.update_db_title_record(my_cursor, record_to_scan)
                my_connection.commit()

        if (PROCESS_TASK & 4) or (PROCESS_TASK & 8):
            my_logger.info(rjlog.logt(f_left = f"=== Processing Files ", f_middle = "="))

            scanned_directory = rjgen.get_list_of_files(
                f_source_directory=SOURCE_DIRECTORY,
                f_source_extensions=SOURCE_EXTENSIONS
            )

            my_javlibrary = javscraper.JAVLibrary()
            total = len(scanned_directory)
            count = 0
            for full_filename in scanned_directory:
                count += 1
                filename, file_extension = os.path.splitext(os.path.basename(full_filename))
                try:
                    f_file_xdata = (os.getxattr(full_filename, 'user.javli')).decode("utf-8")
                except:
                    f_file_xdata = None

                try:
                    f_file_xprate = int((os.getxattr(full_filename, 'user.prate')).decode("utf-8"))
                except:
                    f_file_xprate = None

                to_be_scraped, to_be_scraped_count = rjgen.search_for_title(f_input_string = filename, f_javli_override = f_file_xdata)

                progress = f" {count}/{total}"
                my_logger.info(rjlog.logt(f_left = f"Processing '{filename}' ", f_right = progress))

                if to_be_scraped_count >= 0:
                    os.makedirs(TARGET_DIRECTORY + to_be_scraped, exist_ok=True)

                if to_be_scraped_count == 1:
                    metadata_array = rjmeta.download_metadata(
                        f_process_title=to_be_scraped,
                        f_my_logger=my_logger,
                        f_attribute_override=f_file_xdata
                    )

                    metadata_array["prate"] = ARBITRARY_PRATE
                    if f_file_xprate:
                        if f_file_xprate > 0:
                            my_logger.info(rjlog.logt(f"ATT - Found xattr for {filename}.  ({f_file_xprate})"))
                            metadata_array["prate"] = f_file_xprate
                        
                    metadata_array["added_date"] = BATCH_DATETIME
                    metadata_array["location"] = TARGET_DIRECTORY + to_be_scraped + "/" + to_be_scraped + file_extension

                    if ARBITRARY_PRATE >= 0:
                        metadata_array["file_date"] = time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(full_filename)),)
                        metadata_array["status"] = 9 # what number?

                    if ARBITRARY_PRATE < 0:
                        metadata_array["status"] = 7 # what number?

                if to_be_scraped_count == 0:
                    metadata_array = {
                        "code": to_be_scraped,
                        "name": None,
                        "actor": [],
                        "studio": None,
                        "image": None,
                        "genre": [],
                        "url": [],
                        "score": None,
                        "release_date": None,
                        "added_date": BATCH_DATETIME,
                        "file_date": None,
                        "location": TARGET_DIRECTORY + to_be_scraped + "/" + to_be_scraped + file_extension,
                        "subtitles": None,
                        "prate": ARBITRARY_PRATE,
                        "notes": None,
                        "status": None
                    }

                    if ARBITRARY_PRATE >= 0:
                        metadata_array["file_date"] = time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(full_filename)),)
                        metadata_array["status"] = 8 # what number?

                    if ARBITRARY_PRATE < 0:
                        metadata_array["status"] = 6 # what number?

                if to_be_scraped_count >= 0:
                    rjsub.get_localsubtitles(
                        f_subtitle_general=SUBTITLE_GENERAL,
                        f_subtitle_whisper=SUBTITLE_WHISPER,
                        f_target_directory=TARGET_DIRECTORY,
                        f_target_language=TARGET_LANGUAGE,
                        f_process_title=to_be_scraped,
                        f_my_logger=my_logger
                    )

                    if PROCESS_TASK & 4:
                        rjsub.get_subtitlecat(
                            f_target_directory=TARGET_DIRECTORY,
                            f_target_language=TARGET_LANGUAGE,
                            f_process_title=to_be_scraped,
                            f_my_logger=my_logger
                        )

                    metadata_array["subtitles"] = rjsub.get_best_subtitle(
                        f_target_directory=TARGET_DIRECTORY,
                        f_target_language=TARGET_LANGUAGE,
                        f_process_title=to_be_scraped,
                        f_my_logger=my_logger
                    )

                    shutil.move(
                        SOURCE_DIRECTORY + filename + file_extension,
                        TARGET_DIRECTORY + to_be_scraped + "/" + to_be_scraped + file_extension
                    )

                    rjdb.send_to_database(
                        f_metadata_array=metadata_array,
                        f_my_logger=my_logger,
                        f_my_cursor=my_cursor
                    )

                    my_connection.commit()

                    rjdb.send_to_json(
                        f_metadata_array=metadata_array,
                        f_my_logger=my_logger,
                        f_json_filename=f"{TARGET_DIRECTORY}{to_be_scraped}/{to_be_scraped}.json"
                    )

                if to_be_scraped_count < 0:
                    my_logger.warning(rjlog.logt(f"+++++ {filename}{file_extension} - no confirmed match found."))

                my_connection.commit()
                my_logger.info(rjlog.logt("="))

    my_cursor.close()
    my_connection.disconnect()
