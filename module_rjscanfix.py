import os, re, requests, hashlib, time, json, logging, shutil, sys
from requests_html import HTMLSession
from datetime import datetime
import mysql.connector
from javscraper import *

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
#t Add a 'file to the right place' option.  i.e. a source and destination constant. - need to test
## Check TARGET_DIRECTORY exists
#3 Add some more checks, especially things which can go wrong destructively.  examples?
#3 Probably need to do a bit of tidying up with filename fixing now that we have the more advanced fix_file_code function.
## Add a switch on whether to run the 'move down level' function first.  Makes it eaiser than remarking out.
#t Check subtitle flag gets checked when going to a different target.
#9 Turn the whole thing into a module and have a few wrapper scripts.
#? and some logic to check we're not nesting deeper and deeper
#t Make existing subtitles rename to match the main file.  Maybe it already works.
#t Add an affirmative statement that there has been a single, good match.
## Add a recheck for failed downloads (i.e. try 3 times then give a warning).  Make it more resilient and try to look up less. or put them into a wrapper function with resilience added.
#t Add link to results.  As a table (as they can give multiple results?) or just the first result?
#  Semi-modularize (so that the functions run when imported) - started
#  merge metadata and metadata_urls into a single object (makes it easier maybe?)
#  variables in functions should start with 'function' for attributes and 'process' for internal variables.  Also tidy up everything else.
#  each function should return something even if just True/False - add something useful
#  how do we get the logging and databases into the functions?
#  A bit more resilience for failed lookups
#  we need to get f_metadata_urls written to JSON.
#  Make the 'get an confirmed name' process faster and more consistent.  Seems to not do the 6 thing when running on the fix_flat.
## Send verbose logs to a file
#  Reliable recovery from failure (i.e. what to do with a half done file?) make the move the last step?
#       Create a stub record as early as possible?
#       Then populate at the end.
#  Need to make faster.
#       Differentiate between lookup failure and an affirmative null result.
#  Log file to timestamped filename


# a single function to take a filename, positively identify it (with reasonable confident), and return the new filename / ID.
# a single function to move it + preexisting SRT.
# a single function to look for subs, download them and move to target.
# a single function to get its metadata
# a single function to write the metadata to the database

#region Main Functions
def move_down_level(f_base_directory, f_target_directory, f_process_file, f_base_extensions, f_my_logger):
    
    #file_without_extension = re.sub(process_extension, '', process_file, flags=re.IGNORECASE)
    
    folder_list_1 = os.listdir(f_base_directory + f_process_file)
    folder_list_2 = [file for file in folder_list_1 if any(file.endswith(ext) for ext in f_base_extensions)]

    for filename in folder_list_2:
    
        #process_title = fix_file_code(file_without_extension)
        source_file = f_base_directory + f_process_file + "/" + filename
        destination_file = f_target_directory + filename

        f_my_logger.info("MOV - Moving " + source_file + " up a level.")
        os.rename(source_file, destination_file)

        return True

def move_to_directory(f_base_directory, f_target_directory, f_target_language, f_process_file, f_process_extension, f_my_logger):
        
    process_result = False
    source_file_without_extension = re.sub(f_process_extension, '', f_process_file, flags=re.IGNORECASE)
    destination_file_without_extension = (fix_file_code(re.sub(f_process_extension, '', f_process_file, flags=re.IGNORECASE)))
    destination_file_without_extension = (search_for_title(destination_file_without_extension))[0]
    destination_file_without_extension = (fix_file_code(destination_file_without_extension))

    # Create a folder with the same name as the extension if it doesn't exist
    destination_directory = f_target_directory + destination_file_without_extension
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Move the file to the folder
    os.rename(f_base_directory + f_process_file + f_process_extension, destination_directory + "/" + fix_file_code(destination_file_without_extension + f_process_extension))

    file_list = os.listdir(f_base_directory)
    
    for file in file_list:
        if (file.startswith(source_file_without_extension) and file.endswith(f_target_language)):
                os.rename(f_base_directory + file, destination_directory + "/" + fix_file_code(file))
                f_my_logger.debug("MOV - Moving " + file + " from " + f_base_directory + ".")
                f_my_logger.info("MOV - Moved " + file + " to " + destination_directory + "/.")

    f_my_logger.debug("MOV - Moving " + f_process_file + f_process_extension + " from " + f_base_directory + ".")
    f_my_logger.info("MOV - Moved " + f_process_file + f_process_extension + " to " + destination_directory + "/.")
    process_result = destination_file_without_extension

    return process_result

def download_subtitlecat(f_target_directory, f_target_language, f_process_title, f_my_logger):
    
    session = HTMLSession()
    process_directory = f_target_directory + f_process_title + "/"
    f_process_title = fix_file_code(f_process_title)
    process_subtitleavailable = False

    if any(file.endswith(f_target_language) for file in os.listdir(process_directory)):
        f_my_logger.debug("SUB - Existing subtitles found.")
        process_subtitleavailable = True

    f_my_logger.info("SUB - Searching SubtitleCat for " + f_process_title + ".")

    url_level1 = 'https://www.subtitlecat.com/index.php?search=' + f_process_title
    response_level1 = session.get(url_level1)

    table_level1 = response_level1.html.find('table')[0]
    table_level1_entries = [[c.absolute_links for c in row.find('td')][:1] for row in table_level1.find('tr')][1:]

    for table_level1_entry in table_level1_entries:
        table_level1_entry_url = (list(table_level1_entry[0])[0])

        if re.search(f_process_title, table_level1_entry_url, re.IGNORECASE):
            response_level2 = session.get(table_level1_entry_url)
            table_level2 = response_level2.html.xpath('/html/body/div[4]/div/div[2]', first=True)
            if table_level2 is not None:
                for table_level2_entry in table_level2.absolute_links:
                    if re.search(f_target_language, table_level2_entry, re.IGNORECASE):
                        subtitle_url = table_level2_entry
                try:
                    if re.search(f_target_language, subtitle_url, re.IGNORECASE):
                        subtitle_url_check = (requests.head(subtitle_url).status_code)
                        if subtitle_url_check==200:
                            process_subtitleavailable = True
                            f_my_logger.debug("SUB - Subtitle_URL " + subtitle_url + ".")
                            # Split out the filename
                            if subtitle_url.find('/'):
                                subtitle_filename = ((subtitle_url.rsplit('/', 1)[1]).lower())
                            f_my_logger.info("SUB - Downloading " + subtitle_filename + ".")
                            subtitle_download = requests.get(subtitle_url, allow_redirects=True)

                            new_subtitle_filename = re.sub(f_process_title, f_process_title.upper() + "-(SC)", subtitle_filename, flags=re.IGNORECASE)
                            
                            open(process_directory + new_subtitle_filename, 'wb').write(subtitle_download.content)
                            time.sleep(5)
                except:
                    pass

    return process_subtitleavailable

def download_metadata(f_target_directory, f_process_title, f_process_extension, f_process_subtitle_available, f_process_arbitrary_prate, f_my_logger):
    # no metadata
    f_my_logger.info("MET - Search for metadata for " + f_process_title + ".")  
    f_process_title = fix_file_code(f_process_title)
    metadata = my_javlibrary_new_getvideo(f_process_title)
    r_metadata_array = []
    r_metadata_urls = my_javlibrary_new_search(f_process_title)

    if metadata is not None:
        file_location = f_target_directory + f_process_title + "/" + f_process_title + f_process_extension
        release_date = (metadata.release_date).strftime("%Y-%m-%d %H:%M:%S")
        added_date = str((f"{datetime.now():%Y-%m-%d %H:%M:%S}"))
        file_date = time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(file_location)))

        f_my_logger.info("MET - Metadata downloaded for " + f_process_title + ".")          
        r_metadata_array = {'code': metadata.code, \
                            "name": metadata.name, \
                            "actors": metadata.actresses, \
                            "studio": metadata.studio, \
                            "image": metadata.image, \
                            "genres": metadata.genres, \
                            "score": metadata.score, \
                            "release_date": release_date, \
                            "added_date": added_date, \
                            "file_date": file_date, \
                            "location": file_location, \
                            "subtitles": f_process_subtitle_available, \
                            "prate": f_process_arbitrary_prate}
        
        # metadata_json = json.dumps(metadata_array, indent=4)
        # f_my_logger.debug("MET - Write metadata for " + f_process_title + " to local json.")
        # with open(f_target_directory + f_process_title + "/" + f_process_title + ".json", "w") as outfile:
        #     outfile.write(metadata_json)

        # f_my_logger.info("MET - Write metadata for " + f_process_title + " to database.")
        # send_data_to_database(metadata, metadata_urls, (f_target_directory + f_process_title + "/" + f_process_title + f_process_extension), (f_process_subtitle_available), f_process_arbitrary_prate, f_my_cursor)
    else:
        f_my_logger.info("MET - No metadata found for " + f_process_title + ".")
    
    return r_metadata_array, r_metadata_urls

# we need to get f_metadata_urls written too.
def send_data_to_json(f_metadata_array, f_metadata_urls, f_my_logger, f_json_filename):
    f_my_logger.info("MET - Write metadata for " + f_metadata_array['code'] + " to json.")
    metadata_json = json.dumps(f_metadata_array, indent=4)
    with open(f_json_filename, "w") as outfile:
         outfile.write(metadata_json)

# def send_data_to_database(process_metadata, process_metadata_urls, process_location, process_subtitles_avail, process_arbitrary_prate, f_my_logger, f_my_cursor):
def send_data_to_database(f_metadata_array, f_metadata_urls, f_my_logger, f_my_cursor):
    f_my_logger.info("MET - Write metadata for " + f_metadata_array['code'] + " to database.")
    
    my_insert_sql_titles = ("""insert into titles (code
                            ,name
                            ,studio
                            ,image
                            ,score
                            ,release_date
                            ,added_date
                            ,file_date
                            ,location
                            ,subtitles
                            ,prate
                            ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            on duplicate key update name = values(name), studio = values(studio), score = values(score), image = values(image), release_date = values(release_date), added_date = values(added_date), file_date = values(file_date), location = values(location), subtitles = values(subtitles) """)
    
    my_insert_sql_genre = ("""insert into genre (code
                            , description
                            , uid) VALUES (%s, %s, %s)
                            on duplicate key update description = values(description), uid = values(uid) """)
    
    my_insert_sql_actor_link = ("""insert into actor_link (code
                            , name
                            , uid) VALUES (%s, %s, %s)
                            on duplicate key update name = values(name), uid = values(uid) """)
    
    my_insert_sql_title_urls = ("""insert into urls (code
                            , url
                            , uid) VALUES (%s, %s, %s)
                            on duplicate key update url = values(url), uid = values(uid) """)
    
    my_insert_sql_actor = "insert ignore into actor (name) VALUES (%s)"
                 
    f_my_cursor.execute(my_insert_sql_titles, \
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

    for g in f_metadata_array['genres']:
        hash_input = (f_metadata_array['code'] + g).encode()
        hash_output = hashlib.md5(hash_input).hexdigest()
        f_my_cursor.execute(my_insert_sql_genre, (f_metadata_array['code'], g, hash_output))

    for a in f_metadata_array['actors']:
        hash_input = (f_metadata_array['code'] + a).encode()
        hash_output = hashlib.md5(hash_input).hexdigest()
        f_my_cursor.execute(my_insert_sql_actor_link, (f_metadata_array['code'], a, hash_output))
        f_my_cursor.execute(my_insert_sql_actor, (a,))

    for u in f_metadata_urls:
        hash_input = (f_metadata_array['code'] + u).encode()
        hash_output = hashlib.md5(hash_input).hexdigest()
        f_my_cursor.execute(my_insert_sql_title_urls, (f_metadata_array['code'], u, hash_output))

    return True

def move_files_by_extension(f_source_dir, f_destination_dir, f_extensions):
    for root, _, files in os.walk(f_source_dir):
        for file in files:
            if any(file.endswith(ext) for ext in f_extensions):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(f_destination_dir, file)

                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

                # Move the file to the destination directory
                shutil.move(source_file_path, destination_file_path)
                # make this a logger
                print(f"Moved: {source_file_path} to {destination_file_path}")

#endregion

#region Wrapped Scraper Functions
def my_javlibrary_new_search(f_input_string):
    
    my_javlibrary = JAVLibrary()
    count = 0
    result = []
    while result == [] and count <= 5:
        try:
            result = my_javlibrary.search(f_input_string)
        except:
            pass
        time.sleep(0.25 * count)
        count = count + 1
    return result

def my_javlibrary_new_getvideo(f_input_string):
    
    my_javlibrary = JAVLibrary()
    count = 0
    result = ""
    while result == "" and count <= 5:
        try:
            result = my_javlibrary.get_video(f_input_string)
        except:
            pass
        time.sleep(0.25 * count)
        count = count + 1
    return result
#endregion

#region Primary Data Functions
def fix_file_code(f_input_string, f_delimiter = "-"):
    letters = ""
    numbers = ""
    suffix = ""
    filename, file_extension = os.path.splitext(f_input_string)
    filename_original = filename
    filename = filename.upper()
    file_extension = file_extension.lower()

    counter = 0
    filename_length = len(filename)
    
    # get letters
    while counter < filename_length:
        char = filename[counter]

        if ord(char) in range(64, 91):
            letters = letters + char
            counter = counter + 1
        if char == f_delimiter:
                counter = counter + 1
                break
        if (ord(char) in range(47, 58)):
                break

    while counter < filename_length:
        char = filename[counter]

        if ord(char) in range(47, 58):
            numbers = numbers + char
            counter = counter + 1
        else:
            break
    
    while counter < filename_length:
        char = filename_original[counter]
        counter = counter + 1
        suffix = suffix + char

    number = int(numbers)

    return f"{letters}{f_delimiter}{number:03}{suffix}{file_extension}"

def search_for_title(f_input_string, f_delimiter = "-"):
    
    filename, file_extension = os.path.splitext(f_input_string)
    filename = filename.upper()
    file_extension = file_extension.lower()
    pattern8 = r'^[A-Za-z]{5}\d{3}$'
    pattern7 = r'^[A-Za-z]{4}\d{3}$'
    pattern6 = r'^[A-Za-z]{3}\d{3}$'
    pattern5 = r'^[A-Za-z]{2}\d{3}$'

    results = []
    filename = re.sub(f_delimiter, '', filename, flags=re.IGNORECASE)
    filename_length = len(filename)

    # Search for 8 character codes.
    counter = 0
    while counter + 7 < filename_length:
        f_input_string = filename[counter:counter + 8]
        if (re.match(pattern8, f_input_string)):
            if my_javlibrary_new_search(f_input_string):
                results.append(filename[counter:counter + 8])
        counter = counter + 1    
    
    # Search for 7 character codes.
    counter = 0
    while counter + 6 < filename_length:
        f_input_string = filename[counter:counter + 7]
        if (re.match(pattern7, f_input_string)):
            if my_javlibrary_new_search(f_input_string):
                results.append(filename[counter:counter + 7])
        counter = counter + 1

    # Search for 6 character codes.
    counter = 0
    while counter + 5 < filename_length:
        f_input_string = filename[counter:counter + 6]
        if (re.match(pattern6, f_input_string)):
            if my_javlibrary_new_search(f_input_string):
                results.append(filename[counter:counter + 6])
        counter = counter + 1

    # Search for 5 character codes.
    counter = 0
    while counter + 4 < filename_length:
        f_input_string = filename[counter:counter + 5]
        if (re.match(pattern5, f_input_string)):
            if my_javlibrary_new_search(f_input_string):
                results.append(filename[counter:counter + 5])
        counter = counter + 1
    results = remove_substrings(results)

    return results
#endregion

#region General Purpose Functions
def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",datefmt="%Y-%m-%d %H:%M:%S"))
    console_handler.setLevel(logging.INFO)
    return console_handler

def get_file_handler():
    file_handler = logging.FileHandler("./logs/log.log", mode='w')
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",datefmt="%Y-%m-%d %H:%M:%S"))
    file_handler.setLevel(logging.DEBUG)
    return file_handler

def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    #logger.addHandler(get_syslog_handler())
    return logger

def remove_substrings(f_strings):
    # Sort the strings by length in descending order
    f_strings.sort(key=len, reverse=True)
    result = []
    # Iterate through the sorted strings
    for s in f_strings:
        # Check if the current string is a substring of any previously added string
        is_substring = any(s in r for r in result)
        # If it's not a substring of any previous string, add it to the result
        if not is_substring:
            result.append(s)
    return result

def get_list_of_files(f_base_directory, f_base_extensions):
    
    folder_list_1 = os.listdir(f_base_directory)
    folder_list_2 = [file for file in folder_list_1 if any(file.endswith(ext) for ext in f_base_extensions)]
    folder_list_3 = []

    for file in folder_list_2:
        filename, file_extension = os.path.splitext(os.path.basename(file))
        folder_list_3.append(file)

    return folder_list_3
#endregion