import os, re, requests, hashlib, time, json, logging, shutil, sys
from requests_html import HTMLSession
from datetime import datetime
import mysql.connector
from javscraper import *

#  https://colab.research.google.com/github/richardjj27/WhisperWithVAD

## add a rerun option + re-get json - done by creating a move down a level function
## how about putting all the jsons in a central folder too? - done
## send results to a database - done
## logging for output - done
## add subtitle available attribute - done
## get date working in metadata
## actress to actor - done
## check if incumbent subs exist, so may the subs_avaiable setting True regardless of SC. - done
## if it can't be found, don't move it - just skip
## multiple file extensions?  (MP4, MKV, AVI)
## If it doesn't exist, create an actor row. Needs Testing - seems to be working - test a bit more.
## Fix/Rename the 'moved' subtitle file. Exclude TARGET_LANGUAGE or make the filename fix (-) only work with the first set of letters and numbers. Right now, it is stripping the target language so be careful. - done?  if it works, code can be easier.
## Add a 'file to the right place' option.  i.e. a source and destination constant. - need to test
## Check TARGET_DIRECTORY exists
#3 Add some more checks, especially things which can go wrong destructively.  examples?
## Probably need to do a bit of tidying up with filename fixing now that we have the more advanced fix_file_code function.
## Add a switch on whether to run the 'move down level' function first.  Makes it eaiser than remarking out.
## Check subtitle flag gets checked when going to a different target.
## Turn the whole thing into a module and have a few wrapper scripts.
#? and some logic to check we're not nesting deeper and deeper
## Make existing subtitles rename to match the main file.  Maybe it already works.
## Add an affirmative statement that there has been a single, good match.
## Add a recheck for failed downloads (i.e. try 3 times then give a warning).  Make it more resilient and try to look up less. or put them into a wrapper function with resilience added.
## Add link to results.  As a table (as they can give multiple results?) or just the first result?
## Semi-modularize (so that the functions run when imported) - started
#+ Variables in functions should start with 'f_' for attributes and 'p_' for internal variables.  Also tidy up everything else.
## each function should return something even if just True/False - add something useful
## how do we get the logging and databases into the functions?
#  A bit more resilience for failed lookups.  We fail non-destructively now but it'd be nice to have some retries for URL lookups etc.
## we need to get f_metadata_url written to JSON.
## Make the 'get a confirmed name' process faster and more consistent.  Seems to not do the 6 thing when running on the fix_flat.
## Send verbose logs to a file
## Reliable recovery from failure (i.e. what to do with a half done file?) make the move the last step?
##      Create a stub record as early as possible?
##      Then populate at the end.
##      or do the invasive tasks last
## Need to make faster.
##       Differentiate between lookup failure and an affirmative null result.
## Log file to timestamped filename
## if a strict <filename>-<target langugage> file doesn't already exist copy the largest srt to make it.
## Now retrieves subtitles from a local store if they exist and appends a (LR) suffix.
## get rid of pointless pass commands.
## Removed unused variables (especially from functions)
## Add a move/copy option to the below, with MOVE as default to 'move_files_by_extension' function.  Rename it too.
#  shutil.move instead of os.rename
#  Standardize function argument order.
#+ Check to see what is searched for matches what is found HUNT014 > HUNT146, for example
#  Move the functions into processed order.
#  Standardise on SOURCE (base) and TARGET (destination)

#region Main Functions
def move_down_level(f_target_directory, f_target_directory, f_process_file, f_target_extensions, f_my_logger):
    p_folder_list_1 = os.listdir(f_target_directory + f_process_file)
    p_folder_list_2 = [p_file for p_file in p_folder_list_1 if any(p_file.endswith(ext) for ext in f_target_extensions)]

    for p_filename in p_folder_list_2:
        p_source_file = f_target_directory + f_process_file + "/" + p_filename
        p_target_path = f_target_directory + p_filename

        f_my_logger.info("MOV - Moving " + p_source_file + " up a level.")
        pass
        shutil.move(p_source_file, p_target_path)

        return True

def get_list_of_files(f_target_directory, f_target_extensions):    
    p_folder_list_1 = os.listdir(f_target_directory)
    p_folder_list_2 = [file for file in p_folder_list_1 if any(file.endswith(ext) for ext in f_target_extensions)]
    p_folder_list_3 = []

    for file in p_folder_list_2:
        filename, file_extension = os.path.splitext(os.path.basename(file))
        p_folder_list_3.append(f_target_directory + file)

    return p_folder_list_3

def get_localsubtitle(f_subtitle_repository, f_target_directory, f_process_title, f_subtitle_available, f_my_logger):
    p_process_title = fix_file_code(f_process_title)

    if (os.path.isfile(f_subtitle_repository + p_process_title + ".srt")):
        f_my_logger.info("SUB - Found " + p_process_title + ".srt" + " locally.")
        shutil.copy(f_subtitle_repository + p_process_title + ".srt", f_target_directory + p_process_title + "/" + p_process_title + "-(LR).srt")
        if f_subtitle_available == 0:
            f_subtitle_available = 2

    return f_subtitle_available

def download_subtitlecat(f_target_directory, f_target_language, f_process_title, f_subtitle_available, f_my_logger):
    p_session = HTMLSession()
    f_process_title = fix_file_code(f_process_title)
    p_target_directory = f_target_directory + f_process_title + "/"

    # 0 - no subs
    # 1 - SubtitleCat Subs
    # 2 - Found Subs

    # This bit needs to be moved.
    if any(file.endswith(f_target_language) for file in os.listdir(p_target_directory)):
        f_my_logger.debug("SUB - Existing subtitles found.")
        f_subtitle_available = 1

    f_my_logger.info("SUB - Searching SubtitleCat for '" + f_process_title + "'.")

    p_url_level1 = 'https://www.subtitlecat.com/index.php?search=' + f_process_title
    p_response_level1 = p_session.get(p_url_level1)

    #see to get a few errors on this line below.
    p_table_level1 = p_response_level1.html.find('table')[0]
    p_table_level1_entries = [[c.absolute_links for c in row.find('td')][:1] for row in p_table_level1.find('tr')][1:]

    for p_table_level1_entry in p_table_level1_entries:
        p_table_level1_entry_url = (list(p_table_level1_entry[0])[0])

        if re.search(f_process_title, p_table_level1_entry_url, re.IGNORECASE):
            p_response_level2 = p_session.get(p_table_level1_entry_url)
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
                            p_count = p_count + 1
                            if p_subtitle_url_check == 200:
                                f_subtitle_available = 1
                                f_my_logger.debug("SUB - Subtitle_URL " + p_subtitle_url + ".")
                                # Split out the filename
                                if p_subtitle_url.find('/'):
                                    p_subtitle_filename = ((p_subtitle_url.rsplit('/', 1)[1]).lower())
                                f_my_logger.info("SUB - Downloading " + p_subtitle_filename + ".")
                                p_subtitle_download = requests.get(p_subtitle_url, allow_redirects=True)
                                p_new_subtitle_filename = re.sub(f_process_title, f_process_title.upper() + "-(SC)", p_subtitle_filename, flags=re.IGNORECASE)
                                open(p_target_directory + p_new_subtitle_filename, 'wb').write(p_subtitle_download.content)
                                time.sleep(1)
                                break
                except:
                    pass

    p_file_list = get_list_of_files(p_target_directory, [f_target_language])

    p_biggest_file_size = 0
    p_biggest_file_name = ""

    for p_file in p_file_list:
        if os.path.getsize(p_file) > p_biggest_file_size:
            p_biggest_file_name = p_file
            p_biggest_file_size = os.path.getsize(p_file)

    if (p_biggest_file_size > 0) and not (os.path.isfile(p_target_directory + f_process_title + "-" + f_target_language)):
        f_my_logger.info("SUB - Creating " + f_process_title + "-" + f_target_language + " as default subtitle file.")  
        shutil.copy(p_biggest_file_name, (p_target_directory + f_process_title + "-" + f_target_language))
        f_subtitle_available = 1

    return f_subtitle_available

def download_metadata(f_process_title, f_subtitle_available, f_arbitrary_prate, f_my_logger):
    f_my_logger.info("MET - Searching web for '" + f_process_title + "' metadata.")  
    f_process_title = fix_file_code(f_process_title)
    p_metadata = my_javlibrary_new_getvideo(f_process_title)
    p_metadata_array = []
    p_metadata_url = my_javlibrary_new_search(f_process_title)

    if p_metadata is not None:
        p_release_date = (p_metadata.release_date).strftime("%Y-%m-%d %H:%M:%S")
        p_added_date = str((f"{datetime.now():%Y-%m-%d %H:%M:%S}"))

        f_my_logger.info("MET - Metadata downloaded for '" + f_process_title + "'.")          
        p_metadata_array = {'code': p_metadata.code, \
                            "name": p_metadata.name, \
                            "actor": p_metadata.actresses, \
                            "studio": p_metadata.studio, \
                            "image": p_metadata.image, \
                            "genre": p_metadata.genres, \
                            "score": p_metadata.score, \
                            "release_date": p_release_date, \
                            "added_date": p_added_date, \
                            "file_date": None, \
                            "location": None, \
                            "subtitles": f_subtitle_available, \
                            "prate": f_arbitrary_prate}
    else:
        f_my_logger.info("MET - No metadata found for '" + f_process_title + "'.")
    
    return p_metadata_array, p_metadata_url

def move_to_directory(f_target_directory, f_target_directory, f_target_language, f_process_file, f_process_extension, f_my_logger, f_metadata_array):
    p_result = False
    p_file_match_list = search_for_title(f_process_file)

    if len(p_file_match_list) == 1:
        p_file_match = fix_file_code(p_file_match_list[0])
        p_target_directory = f_target_directory + p_file_match
        if not os.path.exists(p_target_directory):
            os.makedirs(p_target_directory)

        shutil.move (f_target_directory + f_process_file + f_process_extension, p_target_directory + "/" + p_file_match + f_process_extension)

        if f_metadata_array['prate'] >= 0:     
            f_metadata_array.update({'location': p_target_directory + "/" + p_file_match + f_process_extension})
            f_metadata_array.update({'file_date': time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(p_target_directory + "/" + p_file_match + f_process_extension)))})
        else:
            f_metadata_array.update({'added_date': None})
            f_metadata_array.update({'file_date': None})
            f_metadata_array.update({'location_date': None})
        
        p_prefixes = [fix_file_code(p_file_match, ""), fix_file_code(p_file_match, "-")]
        p_file_list = []

 #if os.path.isfile(entry_path):

        for p_filename in os.listdir(f_target_directory):
            for p_prefix in p_prefixes:
                if p_filename.upper().startswith(p_prefix):
                    if os.path.isfile(os.path.join(f_target_directory, p_filename)):
                        p_file_list.append(p_filename)

        # move other existing files
        for file in p_file_list:
            if (file.endswith(f_target_language)):
                # os.rename(f_target_directory + file, p_target_directory + "/" + fix_file_code(file, "-"))
                shutil.move(f_target_directory + file, p_target_directory + "/" + fix_file_code(file, "-"))
                f_my_logger.debug("MOV - Moving " + file + " from " + f_target_directory + ".")
                f_my_logger.info("MOV - Moved " + file + " to " + p_target_directory + "/.")
                f_metadata_array.update({'subtitles': True})

        f_my_logger.debug("MOV - Moving " + f_process_file + f_process_extension + " from " + f_target_directory + ".")
        f_my_logger.info("MOV - Moved " + f_process_file + f_process_extension + " to " + p_target_directory + "/.")
        p_result = p_file_match

    return f_metadata_array, p_result

# we need to get f_metadata_url written too.
def send_data_to_json(f_metadata_array, f_metadata_url, f_my_logger, f_json_filename):
    f_my_logger.info("MET - Write metadata for '" + f_metadata_array['code'] + "' to json.")
    p_metadata_json = json.dumps(f_metadata_array, indent=4)
    with open(f_json_filename, "w") as outfile:
         outfile.write(p_metadata_json)

# def send_data_to_database(process_metadata, process_metadata_url, process_location, process_subtitles_avail, process_arbitrary_prate, f_my_logger, f_my_cursor):
def send_data_to_database(f_metadata_array, f_metadata_url, f_my_logger, f_my_cursor):
    f_my_logger.info("MET - Write metadata for '" + f_metadata_array['code'] + "' to database.")
    p_my_insert_sql_title = "\
        INSERT INTO title \
            (code, \
            name, \
            studio, \
            image, \
            score, \
            release_date, \
            added_date, \
            file_date, \
            location, \
            subtitles, \
            prate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
        ON DUPLICATE KEY UPDATE \
            name = values(name), \
            studio = values(studio), \
            score = values(score), \
            image = values(image), \
            release_date = values(release_date), \
            file_date = values(file_date), \
            location = values(location), \
            subtitles = values(subtitles)"

    p_my_insert_sql_genre = "\
        INSERT INTO genre \
            (title_code, \
            description, \
            uid) VALUES (%s, %s, %s) \
        ON DUPLICATE KEY UPDATE \
            description = values(description), \
            uid = values(uid) "
    
    p_my_insert_sql_actor_link = "\
        INSERT INTO actor_link \
            (title_code, \
            actor_name, \
            uid) VALUES (%s, %s, %s) \
        ON DUPLICATE KEY UPDATE \
            actor_name = values(actor_name), \
            uid = values(uid) "
    
    p_my_insert_sql_title_url = "\
        INSERT INTO url \
            (title_code, \
            url, \
            uid) VALUES (%s, %s, %s) \
        ON DUPLICATE KEY UPDATE \
            url = values(url), \
            uid = values(uid) "
    
    p_my_insert_sql_actor = "\
        INSERT IGNORE INTO actor \
            (name) VALUES (%s)"

    # we seem to get the occassional (random?) incorrect date/time value for filedate here
    f_my_cursor.execute(p_my_insert_sql_title, \
                       (f_metadata_array['code'], \
                        f_metadata_array['name'], \
                        f_metadata_array['studio'], \
                        f_metadata_array['image'], \
                        f_metadata_array['score'], \
                        f_metadata_array['release_date'], \
                        f_metadata_array['added_date'], \
                        f_metadata_array['file_date'], \
                        f_metadata_array['location'], \
                        f_metadata_array['subtitles'], \
                        f_metadata_array['prate']))

    for g in f_metadata_array['genre']:
        p_hash_input = (f_metadata_array['code'] + g).encode()
        p_hash_output = hashlib.md5(p_hash_input).hexdigest()
        f_my_cursor.execute(p_my_insert_sql_genre, (f_metadata_array['code'], g, p_hash_output))

    for a in f_metadata_array['actor']:
        p_hash_input = (f_metadata_array['code'] + a).encode()
        p_hash_output = hashlib.md5(p_hash_input).hexdigest()
        f_my_cursor.execute(p_my_insert_sql_actor_link, (f_metadata_array['code'], a, p_hash_output))
        f_my_cursor.execute(p_my_insert_sql_actor, (a,))

    for u in f_metadata_url:
        p_hash_input = (f_metadata_array['code'] + u).encode()
        p_hash_output = hashlib.md5(p_hash_input).hexdigest()
        f_my_cursor.execute(p_my_insert_sql_title_url, (f_metadata_array['code'], u, p_hash_output))

    return True
           
#endregion

#region Wrapped Scraper Functions
def transfer_files_by_extension(f_source_directory, f_target_directory, f_extensions, f_my_logger, f_processmode='MOVE'):
    for root, _, files in os.walk(f_source_directory):
        for file in files:
            if any(file.endswith(ext) for ext in f_extensions):
                p_source_directory = os.path.join(root, file)
                p_target_directory = os.path.join(f_target_directory, file)

                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(p_target_directory), exist_ok=True)

                # Move the file to the destination directory
                if (f_processmode == "MOVE"):                
                    shutil.move(p_source_directory, p_target_directory)

                # ...or copy.
                if (f_processmode == "COPY"):                
                    shutil.copy(p_source_directory, p_target_directory)

                f_my_logger.info("MET - Transferred to " + p_target_directory + ".")
    return True

def my_javlibrary_new_search(f_input_string):
    p_my_javlibrary = JAVLibrary()
    p_count = 0
    p_result = []
    while p_result == [] and p_count <= 5:
        try:
            p_result = p_my_javlibrary.search(f_input_string)
            p_count = 6
        except:
            time.sleep(0.25 * p_count)
        p_count = p_count + 1
    return p_result

def my_javlibrary_new_getvideo(f_input_string):
    p_my_javlibrary = JAVLibrary()
    p_count = 0
    p_result = ""
    while p_result == "" and p_count <= 5:
        try:
            p_result = p_my_javlibrary.get_video(f_input_string)
        except:
            pass
        time.sleep(0.25 * p_count)
        p_count = p_count + 1
    pass    
    return p_result
#endregion

#region Primary Data Functions
def fix_file_code(f_input_string, f_delimiter = "-"):
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
            p_counter = p_counter + 1
        if ord(p_char) in range(47, 58):
            break
        if ord(p_char) not in range(64, 91):
            p_counter = p_counter + 1
            break

    # get numbers
    while p_counter < p_filename_length:
        p_char = p_filename[p_counter]

        if ord(p_char) in range(47, 58):
            p_numbers = p_numbers + p_char
        else:
            break
        p_counter = p_counter + 1

    while p_counter < p_filename_length:
        p_char = p_filename_original[p_counter]
        p_counter = p_counter + 1
        p_suffix = p_suffix + p_char

    p_number = int(p_numbers)

    return f"{p_letters}{f_delimiter}{p_number:03}{p_suffix}{p_file_extension}"

def search_for_title(f_input_string, f_delimiter = "-"): 
    p_filename, p_file_extension = os.path.splitext(f_input_string)
    p_filename = p_filename.upper()
    p_file_extension = p_file_extension.lower()
    p_pattern8 = r'^[A-Za-z]{5}\d{3}$'
    p_pattern7 = r'^[A-Za-z]{4}\d{3}$'
    p_pattern6 = r'^[A-Za-z]{3}\d{3}$'
    p_pattern5 = r'^[A-Za-z]{2}\d{3}$'

    p_results = []
    p_filename = re.sub(f_delimiter, '', p_filename, flags=re.IGNORECASE)
    p_filename_length = len(p_filename)

    # Search for 8 character codes.
    p_counter = 0
    while p_counter + 7 < p_filename_length:
        f_input_string = p_filename[p_counter:p_counter + 8]
        #print(f_input_string)
        if (re.match(p_pattern8, f_input_string)):
            if my_javlibrary_new_getvideo(f_input_string):
                p_results.append(p_filename[p_counter:p_counter + 8])
        p_counter = p_counter + 1    
    
    # Search for 7 character codes.
    p_counter = 0
    while p_counter + 6 < p_filename_length:
        f_input_string = p_filename[p_counter:p_counter + 7]
        #print(f_input_string)
        if (re.match(p_pattern7, f_input_string)):
            if my_javlibrary_new_getvideo(f_input_string):
                p_results.append(p_filename[p_counter:p_counter + 7])
        p_counter = p_counter + 1

    # Search for 6 character codes.
    p_counter = 0
    while p_counter + 5 < p_filename_length:
        f_input_string = p_filename[p_counter:p_counter + 6]
        #print(f_input_string)
        if (re.match(p_pattern6, f_input_string)):
            if my_javlibrary_new_getvideo(f_input_string):
                p_results.append(p_filename[p_counter:p_counter + 6])
        p_counter = p_counter + 1

    # Search for 5 character codes.
    p_counter = 0
    while p_counter + 4 < p_filename_length:
        f_input_string = p_filename[p_counter:p_counter + 5]
        #print(f_input_string)
        if (re.match(p_pattern5, f_input_string)):
            if my_javlibrary_new_getvideo(f_input_string):
                p_results.append(p_filename[p_counter:p_counter + 5])
        p_counter = p_counter + 1
    p_results = remove_substrings(p_results)
    
    if p_counter > 0:
        p_value1 = fix_file_code(p_results[0])
        p_value2 = (my_javlibrary_new_getvideo(p_value1)).code
        if (p_value1 != p_value2):
            p_results = []
    
    pass

    return p_results
#endregion

#region General Purpose Functions
def get_console_handler():
    p_console_handler = logging.StreamHandler(sys.stdout)
    p_console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",datefmt="%Y-%m-%d %H:%M:%S"))
    p_console_handler.setLevel(logging.INFO)
    return p_console_handler

def get_file_handler():
    p_file_handler = logging.FileHandler('./logs/{:%Y-%m-%d_%H.%M.%S}.log'.format(datetime.now()), mode='w')
    #p_file_handler = logging.FileHandler("./logs/log.log", mode='w')
    p_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",datefmt="%Y-%m-%d %H:%M:%S"))
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

#endregion