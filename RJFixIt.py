import sys, os, re, requests, json, logging, time, hashlib
import mysql.connector
from requests_html import HTMLSession
from javscraper import *

# Define the directory you want to start the search + the file extension + language suffix
BASE_DIRECTORY = "/mnt/multimedia/Other/RatedFinalJ/Series/"
TARGET_DIRECTORY = BASE_DIRECTORY
TARGET_EXTENSIONS = [".mkv", ".mp4", ".avi"]
TARGET_LANGUAGE = "en.srt"
ARBITRARY_PRATE = 0
REDO_FILES = False

## add a rerun option + re-get json - done by creating a move down a level function
#? and some logic to check we're not nesting deeper and deeper
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
#3 Add some more checks, especially things which can go wrong destructively.  example?
#3 Probably need to do a bit of tidying up with filename fixing now that we have the more advanced fix_file_code function.
## Add a switch on whether to run the 'move down level' function first.  Makes it eaiser than remarking out.
#t Check subtitle flag gets checked when going to a different target.
#9 Turn the whole thing into a module and have a few wrapper scripts.
#t Make existing subtitles rename to match the main file.  Maybe it already works.
#1 Add an affirmative statement that there has been a single, good match.
#1 Add a recheck for failed downloads (i.e. try 3 times then give a warning).  Make it more resilient and try to look up less. or put them into a wrapper function with resilience added.
#1 Add link to results.  As a table (as they can give multiple results?) or just the first result?

def move_to_directory(process_file, process_extension):
    process_result = False
    source_file_without_extension = re.sub(process_extension, '', process_file, flags=re.IGNORECASE)
    destination_file_without_extension = (fix_file_code(re.sub(process_extension, '', process_file, flags=re.IGNORECASE)))
    destination_file_without_extension = (search_for_title(destination_file_without_extension))[0]
    destination_file_without_extension = (fix_file_code(destination_file_without_extension))

    # Create a folder with the same name as the extension if it doesn't exist
    destination_directory = TARGET_DIRECTORY + destination_file_without_extension
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Move the file to the folder
    os.rename(BASE_DIRECTORY + process_file + process_extension, destination_directory + "/" + fix_file_code(destination_file_without_extension + process_extension))

    file_list = os.listdir(BASE_DIRECTORY)
    
    for file in file_list:
        if (file.startswith(source_file_without_extension) and file.endswith(TARGET_LANGUAGE)):
                os.rename(BASE_DIRECTORY + file, destination_directory + "/" + fix_file_code(file))
                #shutil.move(process_directory + file, destination_directory)
                my_logger.debug("MOV - Moving " + file + " from " + BASE_DIRECTORY + ".")
                my_logger.info("MOV - Moved " + file + " to " + destination_directory + "/.")

    my_logger.debug("MOV - Moving " + process_file + process_extension + " from " + BASE_DIRECTORY + ".")
    my_logger.info("MOV - Moved " + process_file + process_extension + " to " + destination_directory + "/.")
    process_result = destination_file_without_extension

    return process_result

def fix_file_code(input_string, delimiter = "-"):
    letters = ""
    numbers = ""
    suffix = ""
    filename, file_extension = os.path.splitext(input_string)
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
        if char == delimiter:
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

    return f"{letters}{delimiter}{number:03}{suffix}{file_extension}"

def search_for_title(input_string, delimiter = "-"):
    filename, file_extension = os.path.splitext(input_string)
    filename = filename.upper()
    file_extension = file_extension.lower()
    pattern8 = r'^[A-Za-z]{5}\d{3}$'
    pattern7 = r'^[A-Za-z]{4}\d{3}$'
    pattern6 = r'^[A-Za-z]{3}\d{3}$'
    pattern5 = r'^[A-Za-z]{2}\d{3}$'

    results = []
    filename = re.sub(delimiter, '', filename, flags=re.IGNORECASE)
    filename_length = len(filename)

    # Search for 8 character codes.
    counter = 0
    while counter + 7 < filename_length:
        input_string = filename[counter:counter + 8]
        if (re.match(pattern8, input_string)):
            if my_javlibrary.search(input_string):
                results.append(filename[counter:counter + 8])
        counter = counter + 1    
    
    # Search for 7 character codes.
    counter = 0
    while counter + 6 < filename_length:
        input_string = filename[counter:counter + 7]
        if (re.match(pattern7, input_string)):
            if my_javlibrary.search(input_string):
                results.append(filename[counter:counter + 7])
        counter = counter + 1

    # Search for 6 character codes.
    counter = 0
    while counter + 5 < filename_length:
        input_string = filename[counter:counter + 6]
        if (re.match(pattern6, input_string)):
            if my_javlibrary.search(input_string):
                results.append(filename[counter:counter + 6])
        counter = counter + 1

    # Search for 5 character codes.
    counter = 0
    while counter + 4 < filename_length:
        input_string = filename[counter:counter + 5]
        if (re.match(pattern5, input_string)):
            if my_javlibrary.search(input_string):
                results.append(filename[counter:counter + 5])
        counter = counter + 1

    results = remove_substrings(results)

    return results

def remove_substrings(strings):
    # Sort the strings by length in descending order
    strings.sort(key=len, reverse=True)
    
    # Initialize a list to store non-substring strings
    result = []
    
    # Iterate through the sorted strings
    for s in strings:
        # Check if the current string is a substring of any previously added string
        is_substring = any(s in r for r in result)
        
        # If it's not a substring of any previous string, add it to the result
        if not is_substring:
            result.append(s)
    
    return result

def download_subtitlecat(process_title):
    process_directory = TARGET_DIRECTORY + process_title + "/"
    process_title = fix_file_code(process_title)
    session = HTMLSession()
    process_subtitleavailable = False

    if any(file.endswith(TARGET_LANGUAGE) for file in os.listdir(process_directory)):
        my_logger.debug("SUB - Existing subtitles found.")
        process_subtitleavailable = True

    my_logger.info("SUB - Searching SubtitleCat for " + process_title + ".")

    url_level1 = 'https://www.subtitlecat.com/index.php?search=' + process_title
    response_level1 = session.get(url_level1)

    table_level1 = response_level1.html.find('table')[0]
    table_level1_entries = [[c.absolute_links for c in row.find('td')][:1] for row in table_level1.find('tr')][1:]

    for table_level1_entry in table_level1_entries:
        table_level1_entry_url = (list(table_level1_entry[0])[0])

        if re.search(process_title, table_level1_entry_url, re.IGNORECASE):
            response_level2 = session.get(table_level1_entry_url)
            table_level2 = response_level2.html.xpath('/html/body/div[4]/div/div[2]', first=True)
            if table_level2 is not None:
                for table_level2_entry in table_level2.absolute_links:
                    if re.search(TARGET_LANGUAGE, table_level2_entry, re.IGNORECASE):
                        subtitle_url = table_level2_entry
                try:
                    if re.search(TARGET_LANGUAGE, subtitle_url, re.IGNORECASE):
                        subtitle_url_check = (requests.head(subtitle_url).status_code)
                        if subtitle_url_check==200:
                            process_subtitleavailable = True
                            my_logger.debug("SUB - Subtitle_URL " + subtitle_url + ".")
                            # Split out the filename
                            if subtitle_url.find('/'):
                                subtitle_filename = ((subtitle_url.rsplit('/', 1)[1]).lower())
                            my_logger.info("SUB - Downloading " + subtitle_filename + ".")
                            subtitle_download = requests.get(subtitle_url, allow_redirects=True)

                            new_subtitle_filename = re.sub(process_title, process_title.upper() + "-(SC)", subtitle_filename, flags=re.IGNORECASE)
                            
                            open(process_directory + new_subtitle_filename, 'wb').write(subtitle_download.content)
                            time.sleep(5)
                except:
                    pass

    return process_subtitleavailable

def download_metadata(process_title, process_extension, process_subtitle_available):
    process_title = fix_file_code(process_title)
    metadata = my_javlibrary.get_video(process_title)

    if metadata is not None:
        release_date = (metadata.release_date).strftime("%Y-%m-%d")
        my_logger.info("MET - Downloading metadata for " + process_title + ".")  
        
        metadata_array = {"Code": metadata.code, "Name": metadata.name, "Actor": metadata.actresses, "Studio": metadata.studio, "Image": metadata.image, "Genres": metadata.genres, "Score": metadata.score, "ReleaseDate": release_date, "Location": TARGET_DIRECTORY + process_title + "/" + process_title + process_extension, "Subtitles": process_subtitle_available}
        metadata_json = json.dumps(metadata_array, indent=4)

        my_logger.info("MET - Write metadata for " + process_title + " to local json.")
        with open(TARGET_DIRECTORY + process_title + "/" + process_title + ".json", "w") as outfile:
            outfile.write(metadata_json)

        my_logger.info("MET - Write metadata for " + process_title + " to database.")
        send_data_to_database(metadata, (TARGET_DIRECTORY + process_title + "/" + process_title + process_extension), (process_subtitle_available))
    else:
        my_logger.info("MET - No metadata for " + process_title + ".")

def send_data_to_database(process_metadata, process_location, process_subtitles_avail):
    my_insert_sql_titles = ("""insert into titles (code
                            ,name
                            ,studio
                            ,image
                            ,score
                            ,release_date
                            ,location
                            ,subtitles
                            ,prate
                            ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            on duplicate key update score = values(score), location = values(location), subtitles = values(subtitles) """)
    
    my_insert_sql_genre = ("""insert into genre (code
                            , description
                            , uid) VALUES (%s, %s, %s)
                            on duplicate key update description = values(description), uid = values(uid) """)
    
    my_insert_sql_actor_link = ("""insert into actor_link (code
                            , name
                            , uid) VALUES (%s, %s, %s)
                            on duplicate key update name = values(name), uid = values(uid) """)
    
    my_insert_sql_actor = "insert ignore into actor (name) VALUES (%s)"
                 
    my_cursor.execute(my_insert_sql_titles, (process_metadata.code, process_metadata.name, process_metadata.studio, process_metadata.image, process_metadata.score, process_metadata.release_date, process_location, process_subtitles_avail, ARBITRARY_PRATE))

    for g in process_metadata.genres:
        hash_input = (process_metadata.code + g).encode()
        hash_output = hashlib.md5(hash_input).hexdigest()
        my_cursor.execute(my_insert_sql_genre, (process_metadata.code, g, hash_output))

    for a in process_metadata.actresses:
        hash_input = (process_metadata.code + a).encode()
        hash_output = hashlib.md5(hash_input).hexdigest()
        my_cursor.execute(my_insert_sql_actor_link, (process_metadata.code, a, hash_output))
        my_cursor.execute(my_insert_sql_actor, (a,))

    my_connection.commit()

def move_down_level(process_file):
    #file_without_extension = re.sub(process_extension, '', process_file, flags=re.IGNORECASE)
    
    folder_list_1 = os.listdir(BASE_DIRECTORY + process_file)
    folder_list_2 = [file for file in folder_list_1 if any(file.endswith(ext) for ext in TARGET_EXTENSIONS)]

    for filename in folder_list_2:
    
        #process_title = fix_file_code(file_without_extension)
        source_file = BASE_DIRECTORY + process_file + "/" + filename
        destination_file = TARGET_DIRECTORY + filename

        my_logger.info("MOV - Moving " + source_file + " up a level.")
        os.rename(source_file, destination_file)

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",datefmt="%Y-%m-%d %H:%M:%S"))
   #console_handler.setFormatter(logging.Formatter("%(message)s"))
   return console_handler

def get_syslog_handler():
   syslog_handler = logging.handlers.SysLogHandler(address=(LOGHOST, 514))
   syslog_handler.setFormatter(logging.Formatter("RJMediaScraper %(message)s"))
   return syslog_handler

def get_logger():
   logger = logging.getLogger()
   logger.setLevel(logging.INFO)
   logger.addHandler(get_console_handler())
   #logger.addHandler(get_syslog_handler())
   return logger

def get_list_of_files():
    folder_list_1 = os.listdir(BASE_DIRECTORY)
    folder_list_2 = [file for file in folder_list_1 if any(file.endswith(ext) for ext in TARGET_EXTENSIONS)]
    folder_list_3 = []

    for file in folder_list_2:
        filename, file_extension = os.path.splitext(os.path.basename(file))
        #if(my_javlibrary.search(filename)):
        folder_list_3.append(file)

    return folder_list_3

if __name__ == "__main__":

    my_connection = mysql.connector.connect( 
        user="rjohnson", 
        password="5Nf%GB6r10bD", 
        host="diskstation.hachiko.int", 
        port=3306, 
        database="Multimedia" 
    )
        
    my_javlibrary = JAVLibrary()
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
                move_down_level(filename)

    my_logger.info("================================================================================================")

    scanned_directory = get_list_of_files()
    # Scan through the folder
    for full_filename in scanned_directory:
        #if os.path.isfile(BASE_DIRECTORY + file) and file.lower().endswith(TARGET_EXTENSION):

        filename, file_extension = os.path.splitext(os.path.basename(full_filename))
        my_logger.info("+++++ " + filename + " +++++")
        if len(search_for_title(filename)) == 1:

            to_be_scraped = move_to_directory(filename, file_extension)
            subtitle_available = download_subtitlecat(to_be_scraped)
            download_metadata(to_be_scraped, file_extension, subtitle_available)
        else:
            my_logger.info("Skipping.  Number of results : " + str(len(search_for_title(filename))))


        my_logger.info("================================================================================================")

    my_cursor.close()




    
