import os
import re
import requests
import hashlib
import time
import json
import logging
import shutil
import sys
from requests_html import HTMLSession
from datetime import datetime
import mysql.connector
from javscraper import *

# region Main Functions


def move_up_level(f_source_directory, f_target_directory, f_process_filename, f_source_extensions, f_my_logger):
    p_folder_list_1 = os.listdir(f_source_directory + f_process_filename)
    p_folder_list_2 = [filename for filename in p_folder_list_1 if any(filename.endswith(ext) for ext in f_source_extensions)]

    for p_filename in p_folder_list_2:
        p_source_filename = f_source_directory + f_process_filename + "/" + p_filename
        p_target_directory = f_source_directory + f_process_filename + "/"
        p_target_filename = f_target_directory + p_filename
        
        f_my_logger.info(f"MOV - Moving {p_source_filename} back a level.")
        os.makedirs(p_target_directory, exist_ok=True)
        shutil.move(p_source_filename, p_target_filename)

        return True


def get_list_of_files(f_source_directory, f_source_extensions):
    p_folder_list_1 = os.listdir(f_source_directory)
    p_folder_list_2 = [f_source_directory + filename for filename in p_folder_list_1 if any(filename.endswith(extension) for extension in f_source_extensions)]

    p_folder_list_2.sort()

    return p_folder_list_2


def get_localsubtitles(f_subtitle_general, f_subtitle_whisper, f_target_directory, f_target_language, f_process_title, f_my_logger):
    p_process_title = search_for_title(f_process_title)

    # fix raw whisper filename
    p_whisper_raw = f_subtitle_whisper + p_process_title + "-en Whisper-cleaned.srt"
    p_whisper_raw_fixed = p_whisper_raw.replace("-en Whisper-cleaned", "-(WH)-en")
    try:
        os.rename(p_whisper_raw, p_whisper_raw_fixed)
    except:
        pass

    if (os.path.isfile(f_subtitle_general + p_process_title + ".srt")):
        f_my_logger.info(f"SUB - Found {p_process_title}.srt in 'General'.")
        os.makedirs(f_target_directory + p_process_title, exist_ok=True)
        shutil.copy(f_subtitle_general + p_process_title + ".srt", f_target_directory + p_process_title + "/" + p_process_title + "-(LR).srt")

    if (os.path.isfile(f_subtitle_whisper + p_process_title + ".srt")):
        f_my_logger.info(f"SUB - Found {p_process_title}.srt in 'Whisper'.")
        os.makedirs(f_target_directory + p_process_title, exist_ok=True)
        shutil.copy(f_subtitle_whisper + p_process_title + ".srt", f_target_directory + p_process_title + "/" + p_process_title + "-(WH).srt")

    if (os.path.isfile(f_subtitle_whisper + p_process_title + "." + f_target_language)):
        f_my_logger.info(f"SUB - Found {p_process_title}{f_target_language} in 'Whisper'.")
        os.makedirs(f_target_directory + p_process_title, exist_ok=True)
        shutil.copy(f_subtitle_whisper + p_process_title + "." + f_target_language, f_target_directory + "/" + p_process_title + "/" + p_process_title + "-" + f_target_language)

    if (os.path.isfile(f_subtitle_whisper + p_process_title + "-(WH)-" + f_target_language)):
        f_my_logger.info(f"SUB - Found {p_process_title}-(WH)-{f_target_language} in 'Whisper'.")
        os.makedirs(f_target_directory + p_process_title, exist_ok=True)
        shutil.copy(f_subtitle_whisper + p_process_title + "-(WH)-" + f_target_language, f_target_directory + "/" + p_process_title + "/" + p_process_title + "-(WH)-" + f_target_language)

    return True


def get_subtitlecat(f_target_directory, f_target_language, f_process_title, f_my_logger):
    p_session = HTMLSession()
    p_process_title = search_for_title(f_process_title)
    p_target_directory = f_target_directory + p_process_title + "/"

    if any(filename.endswith(f_target_language) for filename in os.listdir(p_target_directory)):
        f_my_logger.debug("SUB - Existing subtitles found.")

    f_my_logger.info(f"SUB - Searching SubtitleCat for '{p_process_title}'.")

    p_url_level1 = 'https://www.subtitlecat.com/index.php?search=' + p_process_title

    pass
    p_counter = 0
    while p_counter < 5:
        try:
            p_response_level1 = p_session.get(p_url_level1, timeout=60, allow_redirects=True)
            break
        except:
            p_counter += 1
            f_my_logger.warning(f"URL - SubtitleCat (L0) not responding.  Try {str(p_counter)} of 5.")
            time.sleep(30)

    if p_counter >= 5:
        f_my_logger.critical("URL - SubtitleCat (L0) connection failed.  Terminating.")
        exit()

    pass

    p_counter = 0
    while p_counter < 5:
        try:
            p_table_level1 = p_response_level1.html.find('table')[0]
            break
        except:
            p_counter += 1
            f_my_logger.warning(f"URL - SubtitleCat (L1) not responding.  Try {str(p_counter)} of 5.")
            time.sleep(30)

    if p_counter >= 5:
        f_my_logger.critical("URL - SubtitleCat (L1) connection failed.  Terminating.")
        exit()

    pass

    p_table_level1_entries = [[c.absolute_links for c in row.find('td')][:1] for row in p_table_level1.find('tr')][1:]

    for p_table_level1_entry in p_table_level1_entries:
        p_table_level1_entry_url = (list(p_table_level1_entry[0])[0])

        if re.search(p_process_title, p_table_level1_entry_url, re.IGNORECASE):
            p_response_level2 = p_session.get(p_table_level1_entry_url, timeout=60, allow_redirects=True)
            p_table_level2 = p_response_level2.html.xpath('/html/body/div[4]/div/div[2]', first=True)
            if p_table_level2 is not None:
                for p_table_level2_entry in p_table_level2.absolute_links:
                    if re.search(f_target_language, p_table_level2_entry, re.IGNORECASE):
                        p_subtitle_url = p_table_level2_entry
                try:
                    if re.search(f_target_language, p_subtitle_url, re.IGNORECASE):
                        p_count = 0
                        while p_count < 5:
                            p_subtitle_url_check = (requests.head(p_subtitle_url).status_code)
                            p_count += 1
                            if p_subtitle_url_check == 200:
                                f_my_logger.debug(
                                    "SUB - Subtitle_URL " + p_subtitle_url + ".")
                                if p_subtitle_url.find('/'):
                                    p_subtitle_filename = ((p_subtitle_url.rsplit('/', 1)[1]).lower())
                                f_my_logger.info(f"SUB - Downloading {p_subtitle_filename}.")
                                p_subtitle_download = requests.get(p_subtitle_url, timeout=60, allow_redirects=True)
                                p_new_subtitle_filename = re.sub(p_process_title, p_process_title.upper() + "-(SC)", p_subtitle_filename, flags=re.IGNORECASE)
                                
                                open(p_target_directory + p_new_subtitle_filename,
                                     'wb').write(p_subtitle_download.content)
                                time.sleep(p_count)
                                break
                except:
                    pass

    return True


def transfer_files_by_extension(f_source_directory, f_target_directory, f_extensions, f_my_logger, f_processmode='MOVE'):
    pass
    for root, _, files in os.walk(f_source_directory):
        pass
        for filename in files:
            pass
            if any(filename.endswith(ext) for ext in f_extensions):
                p_source_filename = os.path.join(root, filename)
                # p_target_directory = os.path.join(f_target_directory, filename)

                # Ensure the destination directory exists
                # os.makedirs(p_target_directory, exist_ok=True)
                pass
                # Move the file to the destination directory
                if (f_processmode == "MOVE"):
                    shutil.move(p_source_filename, f_target_directory)

                # ...or copy.
                if (f_processmode == "COPY"):
                    f_my_logger.info(f"MET - Transferring {filename} to {f_target_directory}.")
                    shutil.copy(p_source_filename, f_target_directory)

                f_my_logger.info(f"MET - Transferred {filename} to {f_target_directory}.")
    return True


def get_best_subtitle(f_target_directory, f_target_language, f_process_title, f_my_logger):
    # determine the subtitle status only here...
    # remove from elsewhere.
    p_process_title = search_for_title(f_process_title)
    p_target_directory = f_target_directory + p_process_title + "/"
    p_filelist = get_list_of_files(p_target_directory, ['.srt'])
    p_biggest_filesize = 0
    p_biggest_filename = ""
    p_subtitle_available = 0

    for p_filename in p_filelist:
        if os.path.getsize(p_filename) > p_biggest_filesize and p_filename.endswith(f_target_language):
            p_biggest_filename = p_filename
            p_biggest_filesize = os.path.getsize(p_filename)

        if p_filename.endswith('.srt') and p_subtitle_available < 7:
            p_subtitle_available = 7

        if p_filename.endswith('-(WH).srt') and p_subtitle_available < 8:
            p_subtitle_available = 8

        if p_filename.endswith(f_target_language):
            p_subtitle_available = 9

    if (p_biggest_filesize > 0) and not (os.path.isfile(p_target_directory + p_process_title + "-" + f_target_language)):
        f_my_logger.info(f"SUB - Creating {p_process_title}-{f_target_language} as default subtitle file.")
        shutil.copy(p_biggest_filename, (p_target_directory + p_process_title + "-" + f_target_language))

    return p_subtitle_available


# def download_metadata(f_process_title, f_my_logger):
#     p_my_javlibrary = JAVLibrary()
#     p_process_title = f_process_title
#     p_metadata = p_my_javlibrary.get_video(p_process_title)
#     p_metadata_url = p_my_javlibrary.search(p_process_title)
#     p_metadata_array = []

#     f_my_logger.info(f"MET - Searching web for '{p_process_title}' metadata.")

#     if p_metadata is not None:
#         p_release_date = (p_metadata.release_date).strftime("%Y-%m-%d")

#         f_my_logger.info(f"MET - Metadata downloaded for '{p_process_title}'.")

#         p_metadata_array = {"code": p_metadata.code,
#                             "name": p_metadata.name,
#                             "actor": p_metadata.actresses,
#                             "studio": p_metadata.studio,
#                             "image": p_metadata.image,
#                             "genre": p_metadata.genres,
#                             "url": p_metadata_url,
#                             "score": p_metadata.score,
#                             "release_date": p_release_date,
#                             "added_date": None,
#                             "file_date": None,
#                             "notes": None,
#                             "location": None,
#                             "subtitles": None,
#                             "prate": None,
#                             "status": None}
#     else:
#         # does this ever get called?
#         f_my_logger.info(f"MET - No metadata found for '{p_process_title}'.")

#     return p_metadata_array


# def move_to_directory(f_source_directory, f_target_directory, f_target_language, f_process_file, f_process_extension, f_my_logger, f_metadata_array):
#     p_file_match = search_for_title(f_process_file)

#     if (p_file_match):
#         p_target_directory = f_target_directory + p_file_match

#         os.makedirs(p_target_directory, exist_ok=True)
#         shutil.move(f_source_directory + f_process_file + f_process_extension,
#                     p_target_directory + "/" + p_file_match + f_process_extension)
#         pass

#         try:
#             p_prate = f_metadata_array['prate']
#         except:
#             p_prate = 0

#         if p_prate >= 0:
#             f_metadata_array.update(
#                 {'location': p_target_directory + "/" + p_file_match + f_process_extension})
#             f_metadata_array.update({'file_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
#                 os.path.getctime(p_target_directory + "/" + p_file_match + f_process_extension)))})
#         else:
#             f_metadata_array.update({'added_date': None})
#             f_metadata_array.update({'file_date': None})
#             f_metadata_array.update({'location_date': None})

#         pass

#         # what is this?  what is 'prefixes' ?
#         p_prefixes = [fix_file_code(p_file_match, ""), fix_file_code(p_file_match, "-")]
#         p_file_list = []

#         for p_filename in os.listdir(f_source_directory):
#             for p_prefix in p_prefixes:
#                 if p_filename.upper().startswith(p_prefix):
#                     if os.path.isfile(os.path.join(f_source_directory, p_filename)):
#                         p_file_list.append(p_filename)

#         # move other existing files
#         for filename in p_file_list:
#             if (filename.endswith(f_target_language)):
#                 print ("making")
#                 os.makedirs(p_target_directory, exist_ok=True)
#                 shutil.move(f_source_directory + filename, p_target_directory + "/" + search_for_title(filename))
#                 f_my_logger.debug("MOV - Moving " + filename + " from " + f_source_directory + ".")
#                 f_my_logger.info("MOV - Moved " + filename + " to " + p_target_directory + "/.")
#                 f_metadata_array.update({'subtitles': 1})

#         f_my_logger.debug("MOV - Moving " + f_process_file + f_process_extension + " from " + f_source_directory + ".")
#         f_my_logger.info("MOV - Moved " + f_process_file + f_process_extension + " to " + p_target_directory + "/.")

#     return f_metadata_array

# we need to get f_metadata_url written too.

# def send_data_to_database(process_metadata, process_metadata_url, process_location, process_subtitles_avail, process_arbitrary_prate, f_my_logger, f_my_cursor):


def send_to_database(f_metadata_array, f_my_logger, f_my_cursor):
    pass
    # if net new 'INSERT', if not, 'UPDATE' - if update, leave prate as is.
    p_my_insert_sql_title = "\
        INSERT INTO title (\
            name, \
            studio, \
            image, \
            score, \
            release_date, \
            added_date, \
            file_date, \
            location, \
            subtitles, \
            prate, \
            notes, \
            status, \
            code) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    p_my_insert_sql_title_u = "\
        UPDATE title SET \
            name = %s, \
            studio = %s, \
            image = %s, \
            score = %s, \
            release_date = %s, \
            added_date = %s, \
            file_date = %s, \
            location = %s, \
            subtitles = %s, \
            prate = %s, \
            notes = %s, \
            status = %s \
            WHERE code = %s;"

    p_my_insert_sql_genre = "\
        INSERT IGNORE INTO genre \
            (description) VALUES (%s);"

    # should we be using IGNORE so much here?
    p_my_insert_sql_genre_title_link = "\
        INSERT INTO genre_title_link \
            (genre_g_id, \
            title_code, \
            guid ) VALUES (%s, %s, %s) \
        ON DUPLICATE KEY UPDATE \
            genre_g_id = values(genre_g_id), \
            title_code = values(title_code), \
            guid = values(guid);"

    p_my_insert_sql_url = "\
        INSERT INTO url \
            (title_code, \
            url, \
            guid) VALUES (%s, %s, %s) \
        ON DUPLICATE KEY UPDATE \
            url = values(url), \
            guid = values(guid);"

    p_my_insert_sql_actor = "\
        INSERT IGNORE INTO actor \
            (name) VALUES (%s);"

    p_my_insert_sql_actor_title_link = "\
        INSERT INTO actor_title_link \
            (actor_a_id, \
            title_code, \
            guid ) VALUES (%s, %s, %s) \
        ON DUPLICATE KEY UPDATE \
            actor_a_id = values(actor_a_id), \
            title_code = values(title_code), \
            guid = values(guid);"

    # we seem to get the occassional (random?) incorrect date/time value for filedate here
    # check if the record exists, if it does...
    # p_my_insert_sql_title = p_my_insert_sql_title.replace("INSERT INTO","UPDATE INTO")
    # print(f"SELECT code FROM title WHERE code = '{f_metadata_array['code']}'")
    f_my_cursor.execute(f"SELECT * FROM title WHERE code = '{f_metadata_array['code']}';")
    p_my_results = f_my_cursor.fetchone()
    pass

    if (p_my_results):
        f_my_logger.info(f"MET - Write updated metadata for '{f_metadata_array['code']}' to database.")
        p_my_insert_sql_title = p_my_insert_sql_title_u
        # the columns we retain when updating a title.
        f_prate = p_my_results['prate']
        f_added_date = p_my_results['added_date']
        f_notes = p_my_results['notes']
        f_location = f_metadata_array['location']

        # we need some logic and extra warning when a duplication or record moves.
        # if current is a real file (i.e. p_rate >=0) and if the existing db record is prate -1, always update and flag the fact that the 'requested' has now been fulfilled.
        # if current is a real file (i.e. p_rate >=0) and if the existing db record is real (i.e. p_rate >=0), but the location is different, check both physcical locations.
        #   if a file exists in both, skip with a highly visible warning alert.
        #   if only exists in one location, update the location of the DB to that one.

        # consider a way to 'format neutralize' the file path prefix when doing location comparisions - a function?

       
    else:
        f_my_logger.info(f"MET - Write new metadata for '{f_metadata_array['code']}' to database.")
        f_prate = f_metadata_array['prate']
        f_added_date = f_metadata_array['added_date']
        f_notes = f_metadata_array['notes']
        f_location = f_metadata_array['location']

    try:
        f_location = f_location.replace("/mnt", "file://diskstation")
    except:
        f_location = ''

    f_my_cursor.execute(p_my_insert_sql_title,
                        (f_metadata_array['name'],
                         f_metadata_array['studio'],
                         f_metadata_array['image'],
                         f_metadata_array['score'],
                         f_metadata_array['release_date'],
                         f_added_date,
                         f_metadata_array['file_date'],
                         f_location,
                         f_metadata_array['subtitles'],
                         f_prate,
                         f_notes,
                         f_metadata_array['status'],
                         f_metadata_array['code']))

    for a in f_metadata_array['actor']:
        p_my_query_sql_actor = f"SELECT a_id FROM actor WHERE name = '{a}';"
        f_my_cursor.execute(p_my_query_sql_actor)
        p_my_results = f_my_cursor.fetchone()

        if p_my_results is None:
            f_my_cursor.execute(p_my_insert_sql_actor, (a,))
            p_a_id = f_my_cursor.lastrowid
        else:
            p_a_id = p_my_results['a_id']

        p_hash_input = (
            f_metadata_array['code'] + str(p_a_id) + "actor_title_link").encode()
        p_hash_output = hashlib.sha1(p_hash_input).hexdigest()
        f_my_cursor.execute(p_my_insert_sql_actor_title_link,
                            (p_a_id,
                             f_metadata_array['code'],
                             p_hash_output))

    for g in f_metadata_array['genre']:
        p_my_query_sql_genre = "SELECT g_id FROM genre WHERE description = '" + g + "';"
        f_my_cursor.execute(p_my_query_sql_genre)
        p_my_results = f_my_cursor.fetchone()

        if p_my_results is None:
            f_my_cursor.execute(p_my_insert_sql_genre, (g,))
            p_g_id = f_my_cursor.lastrowid
        else:
            p_g_id = p_my_results['g_id']
        pass

        p_hash_input = (
            f_metadata_array['code'] + str(p_g_id) + "genre_title_link").encode()
        p_hash_output = hashlib.sha1(p_hash_input).hexdigest()
        f_my_cursor.execute(p_my_insert_sql_genre_title_link,
                            (p_g_id, f_metadata_array['code'], p_hash_output))

    for u in f_metadata_array['url']:
        p_hash_input = (f_metadata_array['code'] + u).encode()
        p_hash_output = hashlib.md5(p_hash_input).hexdigest()
        f_my_cursor.execute(p_my_insert_sql_url, (f_metadata_array['code'], u, p_hash_output))

    return True


def send_to_json(f_metadata_array, f_my_logger, f_json_filename):
    f_my_logger.info(f"MET - Write metadata for '{f_metadata_array['code']}' to json.")
    pass

    try:
        p_location = f_metadata_array['location'].replace("/mnt", "file://diskstation")
    except:
        p_location = ''

    p_metadata_json_array = {"code": f_metadata_array['code'],
                             "name": f_metadata_array['name'],
                             "actor": f_metadata_array['actor'],
                             "studio": f_metadata_array['studio'],
                             "image": f_metadata_array['image'],
                             "genre": f_metadata_array['genre'],
                             "url": f_metadata_array['url'],
                             "score": f_metadata_array['score'],
                             "release_date": f_metadata_array['release_date'],
                             "location": p_location}

    p_metadata_json = json.dumps(p_metadata_json_array, indent=4)
    with open(f_json_filename, "w") as outfile:
        outfile.write(p_metadata_json)

# endregion

# region Wrapped Scraper Functions


# endregion

# region Primary Data Functions


def fix_file_code(f_input_string, f_delimiter="-"):
    # This can probably be simplified with some good regular expressions.
    p_letters = ""
    p_numbers = ""
    p_suffix = ""
    p_filename, p_file_extension = os.path.splitext(f_input_string)
    p_filename_original = p_filename
    p_filename = p_filename.upper()
    p_file_extension = p_file_extension.lower()
    p_counter = 0
    p_filename_length = len(p_filename)

    # get letters
    while p_counter < p_filename_length:
        p_char = p_filename[p_counter]

        if ord(p_char) in range(64, 91):
            p_letters = p_letters + p_char
            p_counter += 1
        if ord(p_char) in range(47, 58):
            break
        if ord(p_char) not in range(64, 91):
            p_counter += 1
            break

    # get numbers
    while p_counter < p_filename_length:
        p_char = p_filename[p_counter]

        if ord(p_char) in range(47, 58):
            p_numbers = p_numbers + p_char
        else:
            break
        p_counter += 1

    while p_counter < p_filename_length:
        p_char = p_filename_original[p_counter]
        p_counter += 1
        p_suffix = p_suffix + p_char

    p_number = int(p_numbers)

    return f"{p_letters}{f_delimiter}{p_number:03}{p_suffix}{p_file_extension}"

# count =  1    =  all good, one confirmed match
# count =  0    =  name looks good, but no scrape.
# count = -n    =  multiple returned matches, skip
# count = -255  =  absolutely nothing found.

def search_for_title(f_input_string):
    f_my_javlibrary = JAVLibrary()
    p_valid = r'([A-Z]){2,}[0-9]{3,}([A-Z])'
    p_strict_valid = r'^([A-Z]{3,5})(\d{3})Z$'
    p_input_string = f_input_string.upper()
    p_input_string = re.sub(r'[^A-Z0-9]', '', p_input_string)
    p_input_string += "Z"

    p_strict_match = (re.match(p_strict_valid, p_input_string))
    p_strict_matched_value = None
    if p_strict_match:
        p_strict_matched_value = p_strict_match.group(1) + '-' + p_strict_match.group(2)
    
    p_substrings = set()
    for p_loop in range(len(p_input_string)):
        p_substring = p_input_string[p_loop:]
        if re.match(p_valid, p_substring):
            p_matched_value = ((re.match(p_valid, p_substring)).group())
            p_matched_value = p_matched_value[:-1]
            p_get_video = (f_my_javlibrary.get_video(p_matched_value))
            if (p_get_video):
                p_substrings.add(p_get_video.code)

    p_result = p_strict_matched_value
    p_result_count = (len(p_substrings))

    if len(p_substrings) > 1:
        p_result = list(p_substrings)[0]
        p_result_count = -(len(p_substrings))

    if len(p_substrings) == 0:
        p_result = p_strict_matched_value
        p_result_count = 0
        if p_strict_matched_value is None:
            p_result_count = -255
    
    return p_result, p_result_count

def get_db_array(f_my_cursor, f_db_query):
    p_my_sql_query = f"SELECT * FROM title {f_db_query} ORDER BY code"
    f_my_cursor.execute(p_my_sql_query)
    p_results = f_my_cursor.fetchall()
    return p_results

def get_db_title_record(f_my_cursor, f_process_filename):
    p_my_sql_query = "SELECT * FROM title WHERE code='" + f_process_filename + "'"
    f_my_cursor.execute(p_my_sql_query)

    p_result = f_my_cursor.fetchone()
    return p_result

def update_db_title_record(f_my_cursor, f_db_record):
    p_my_insert_sql_title = "\
        UPDATE title SET \
            name = %s, \
            studio = %s, \
            image = %s, \
            score = %s, \
            release_date = %s, \
            added_date = %s, \
            file_date = %s, \
            location = %s, \
            subtitles = %s, \
            prate = %s, \
            notes = %s, \
            status = %s \
            WHERE code = %s;"

    f_my_cursor.execute(p_my_insert_sql_title,
                        (f_db_record['name'],
                         f_db_record['studio'],
                         f_db_record['image'],
                         f_db_record['score'],
                         f_db_record['release_date'],
                         f_db_record['added_date'],
                         f_db_record['file_date'],
                         f_db_record['location'],
                         f_db_record['subtitles'],
                         f_db_record['prate'],
                         f_db_record['notes'],
                         f_db_record['status'],
                         f_db_record['code']))

def value_in_list(f_list, f_value):
    p_results = False

    for i in f_list:
        if f_value in i['code']:
            p_results = i
            break
        else:
            p_results = {'code': f_value, 'status': 0, 'location': None}

    return p_results

# endregion

# region General Purpose Functions


def get_console_handler():
    p_console_handler = logging.StreamHandler(sys.stdout)
    p_console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    p_console_handler.setLevel(logging.INFO)
    return p_console_handler


def get_file_handler():
    p_file_handler = logging.FileHandler('./logs/{:%Y-%m-%d_%H.%M.%S}.log'.format(datetime.now()), mode='w')
    p_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    p_file_handler.setLevel(logging.DEBUG)
    return p_file_handler


def get_logger():
    p_logger = logging.getLogger()
    p_logger.setLevel(logging.DEBUG)
    p_logger.addHandler(get_console_handler())
    p_logger.addHandler(get_file_handler())
    return p_logger


def remove_substrings(f_strings):
    # Sort the strings by length in descending order
    f_strings.sort(key=len, reverse=True)
    p_result = []
    # Iterate through the sorted strings
    for s in f_strings:
        # Check if the current string is a substring of any previously added string
        is_substring = any(s in r for r in p_result)
        # If it's not a substring of any previous string, add it to the result
        if not is_substring:
            p_result.append(s)
    return p_result

# endregion
