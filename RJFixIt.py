import sys, os, re, requests, json, logging, time, hashlib, shutil
import mysql.connector
from requests_html import HTMLSession
from javscraper import *

# Define the directory you want to start the search + the file extension + language suffix
BASE_DIRECTORY = "/mnt/multimedia/Other/RatedFinalJ/Series/Bban/"
TARGET_EXTENSION = ".mkv"
TARGET_LANGUAGE = "en.srt"

## add a rerun option + re-get json - done by creating a move down a level function
#  and some logic to check we're not nesting deeper and deeper
## how about putting all the jsons in a central folder too? - done
## send results to a database - done
## logging for output - done
## add subtitle available attribute - done
## get date working in metadata
## actress to actor - done
## check if incumbent subs exist, so may the subs_avaiable setting True regardless of SC. - done

def move_to_directory(process_directory, process_file, process_extension, process_language):
    process_result = ""

    # Get the full path of the file and extract the extension without the dot
    source_file_without_extension = re.sub(process_extension, '', process_file, flags=re.IGNORECASE)
    destination_file_without_extension = (fix_file_code(re.sub(process_extension, '', process_file, flags=re.IGNORECASE)))

    # Create a folder with the same name as the extension if it doesn't exist
    destination_directory = process_directory + destination_file_without_extension
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Move the file to the folder
    os.rename(process_directory + process_file, destination_directory + "/" + fix_file_code(destination_file_without_extension + process_extension))

    file_list = os.listdir(process_directory)
    for file in file_list:
        if (file.startswith(source_file_without_extension) and file.endswith(process_language)):
                shutil.move(process_directory + file, destination_directory)
                my_logger.info("MUL - Moved " + file + " to " + destination_directory + ".")

    my_logger.info("MUL - Moved " + process_file + " to " + destination_directory + ".")
    process_result = destination_file_without_extension
    return process_result

def fix_file_code(input_string, delim = "-"):
    letters = ""
    numbers = ""

    file_name, file_extension = os.path.splitext(input_string)
    file_name = file_name.upper()
    file_extension = file_extension.lower()

    for char in file_name:
        if ord(char) in range(65, 91):
            letters += char
        elif ord(char) in range(48, 58):
            numbers += char

    number = int(numbers)
    return f"{letters}{delim}{number:03}{file_extension}"

def download_subtitlecat(process_directory, process_title, process_language):
    process_directory = process_directory + process_title + "/"
    process_title = fix_file_code(process_title)

    my_logger.info("DLS - Searching SubtitleCat for " + process_title + ".")

    # Create the HTML session
    session = HTMLSession()
    process_subtitleavailable = False

    if any(file.endswith(process_language) for file in os.listdir(process_directory)):
        my_logger.info("DLS - Existing Subtitles Found.")
        process_subtitleavailable = True
    
    url_level1 = 'https://www.subtitlecat.com/index.php?search=' + process_title
    response_level1 = session.get(url_level1)

    table_level1 = response_level1.html.find('table')[0]
    table_level1_entries = [[c.absolute_links for c in row.find('td')][:1] for row in table_level1.find('tr')][1:]

    for table_level1_entry in table_level1_entries:
        table_level1_entry_url = (list(table_level1_entry[0])[0])
        if re.search(process_title, table_level1_entry_url, re.IGNORECASE):
            response_level2 = session.get(table_level1_entry_url)
            table_level2 = response_level2.html.xpath('/html/body/div[4]/div/div[2]', first=True)
            for table_level2_entry in table_level2.absolute_links:
                if re.search(process_language, table_level2_entry, re.IGNORECASE):
                    subtitle_url = table_level2_entry
            try:
                if re.search(process_language, subtitle_url, re.IGNORECASE):
                    subtitle_url_check = (requests.head(subtitle_url).status_code)
                    if subtitle_url_check==200:
                        process_subtitleavailable = True
                        my_logger.debug("DLS - Subtitle_URL " + subtitle_url + ".")
                        # Split out the filename
                        if subtitle_url.find('/'):
                            subtitle_filename = ((subtitle_url.rsplit('/', 1)[1]).lower())
                        my_logger.info("DLS - Downloading " + subtitle_filename + ".")
                        subtitle_download = requests.get(subtitle_url, allow_redirects=True)

                        new_subtitle_filename = re.sub(process_title, process_title.upper() + "-(SC)", subtitle_filename, flags=re.IGNORECASE)
                        
                        open(process_directory + new_subtitle_filename, 'wb').write(subtitle_download.content)
                        time.sleep(10)
            except:
                pass

    return process_subtitleavailable

def download_metadata(process_directory, process_title, process_extension, process_subtitle_available):
    process_title = fix_file_code(process_title)
    metadata = my_javlibrary.get_video(process_title)
    if metadata is not None:
        release_date = (metadata.release_date).strftime("%Y-%m-%d")
        my_logger.info("GMD - Downloading metadata for " + process_title + ".")  
        
        metadata_array = {"Code": metadata.code, "Name": metadata.name, "Actor": metadata.actresses, "Studio": metadata.studio, "Image": metadata.image, "Genres": metadata.genres, "Score": metadata.score, "ReleaseDate": release_date, "Location": process_directory + process_title + "/" + process_title + process_extension, "Subtitles": process_subtitle_available}
        metadata_json = json.dumps(metadata_array, indent=4)

        my_logger.info("GMD - Write metadata for " + process_title + " to json.")
        with open(process_directory + process_title + "/" + process_title + ".json", "w") as outfile:
            outfile.write(metadata_json)

        my_logger.info("GMD - Write metadata for " + process_title + " to database.")
        send_data_to_database(metadata, (process_directory + process_title + "/" + process_title + process_extension), (process_subtitle_available))
    else:
        my_logger.info("GMD - No metadata for " + process_title + ".")

def send_data_to_database(process_metadata, process_location, process_subtitles_avail):
    my_insert_sql_titles = ("""insert into titles (code
                            ,name
                            ,studio
                            ,image
                            ,score
                            ,release_date
                            ,location
                            ,subtitles
                            ) values (%s, %s, %s, %s, %s, %s, %s, %s)
                            on duplicate key update score = values(score), location = values(location), subtitles = values(subtitles) """)
    
    my_insert_sql_genre = "INSERT IGNORE INTO genre (code, description, uid) VALUES (%s, %s, %s)"
    my_insert_sql_actor = "INSERT IGNORE INTO actor (code, name, uid) VALUES (%s, %s, %s)"

    my_cursor.execute(my_insert_sql_titles, (process_metadata.code, process_metadata.name, process_metadata.studio, process_metadata.image, process_metadata.score, process_metadata.release_date, process_location, process_subtitles_avail))

    for g in process_metadata.genres:
        hash_input = (process_metadata.code + g).encode()
        hash_output = hashlib.md5(hash_input).hexdigest()
        my_cursor.execute(my_insert_sql_genre, (process_metadata.code, g, hash_output))

    for a in process_metadata.actresses:
        hash_input = (process_metadata.code + a).encode()
        hash_output = hashlib.md5(hash_input).hexdigest()
        my_cursor.execute(my_insert_sql_actor, (process_metadata.code, a, hash_output))

    my_connection.commit()

def move_down_level(process_directory, process_file, process_extension):
    file_without_extension = re.sub(process_extension, '', process_file, flags=re.IGNORECASE)
    process_title = fix_file_code(file_without_extension)
    source_file = process_directory + process_title + "/" + process_title + process_extension
    destination_file = process_directory + process_title + process_extension
    if os.path.exists(source_file):
        my_logger.info("MDL - Moving " + source_file + " down a level.")
        try:
            os.rename(source_file, destination_file)
        except:
            pass

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",datefmt="%Y-%m-%d %H:%M:%S"))
   #console_handler.setFormatter(logging.Formatter("%(message)s"))
   return console_handler

# def get_syslog_handler():
#    syslog_handler = logging.handlers.SysLogHandler(address=(LOGHOST, 514))
#    syslog_handler.setFormatter(logging.Formatter("RJMediaScraper %(message)s"))
#    return syslog_handler

def get_logger():
   logger = logging.getLogger()
   logger.setLevel(logging.INFO)
   logger.addHandler(get_console_handler())
   #logger.addHandler(get_syslog_handler())
   return logger

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

    my_logger.info("======================================================================================")

    start_dir = os.listdir(BASE_DIRECTORY)

    # Moves the files down level so they get rescanned.
    for file in start_dir:
        if os.path.isdir(BASE_DIRECTORY + file):
            move_down_level(BASE_DIRECTORY, file, TARGET_EXTENSION)

    my_logger.info("======================================================================================")

    time.sleep(10)
    start_dir = os.listdir(BASE_DIRECTORY)

    # Scan through the folder
    for file in start_dir:
        if os.path.isfile(BASE_DIRECTORY + file) and file.lower().endswith(TARGET_EXTENSION):
            my_logger.info("+++++ " + file + " +++++")
            to_be_scraped = move_to_directory(BASE_DIRECTORY, file, TARGET_EXTENSION, TARGET_LANGUAGE)
            subtitle_available = download_subtitlecat(BASE_DIRECTORY, to_be_scraped, TARGET_LANGUAGE)
            download_metadata(BASE_DIRECTORY, to_be_scraped, TARGET_EXTENSION, subtitle_available)
            my_logger.info("======================================================================================")
            pass

    my_cursor.close()




    
