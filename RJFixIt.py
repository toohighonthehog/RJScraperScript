import sys, os, re, requests, json, logging, time, hashlib
import mysql.connector


from requests_html import HTMLSession
from javscraper import *


javlibrary = JAVLibrary()


# add a rerun option + re-get json - done by creating a move down a level function
# and some logic to check we're not nesting deeper and deeper
# how about putting all the jsons in a central folder too? - done
# send results to a database
# colour coding or logging for output - half done
# add subtitle available attribute - done
# get date working in metadata
# DASD677 subs??
# actress to actor

def move_to_directory(process_directory, process_file, process_extension):
    process_result = ""

    # Get the full path of the file and extract the extension without the dot
    file_without_extension = re.sub(process_extension, '', process_file, flags=re.IGNORECASE)
    extension_without_dot = process_extension.strip(".")

    # Create a folder with the same name as the extension if it doesn't exist
    destination_directory = process_directory + insert_hyphen_between_letters_and_numbers(file_without_extension.upper())
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Move the file to the folder
    #print(process_directory + file)
    #print(insert_hyphen_between_letters_and_numbers(destination_directory) + "/" + insert_hyphen_between_letters_and_numbers(file_without_extension).upper() + process_extension.lower())
    os.rename(process_directory + file, insert_hyphen_between_letters_and_numbers(destination_directory) + "/" + insert_hyphen_between_letters_and_numbers(file_without_extension).upper() + process_extension.lower())
    my_logger.info("MUL - Moved " + process_file + " to " + destination_directory + ".")
    process_result = file_without_extension
    
    return process_result

def insert_hyphen_between_letters_and_numbers(input_string):
    # Use regular expression to find all occurrences of letters followed by numbers
    # and insert a hyphen between them
    # it should only be a single hyphen so needs some checking
    result = re.sub(r'([a-zA-Z])(\d)', r'\1-\2', input_string)
    return result

def download_subtitlecat(process_directory, process_title, process_language):
    process_directory = process_directory + process_title + "/"
    process_title = insert_hyphen_between_letters_and_numbers(process_title)

    my_logger.info("DLS - Processing " + process_directory + " (" + process_title + ").")

    # Create the HTML session
    session = HTMLSession()
    process_subtitleavailable = False
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
                        my_logger.info("DLS - Subtitle_URL " + subtitle_url + ".")
                        # Split out the filename
                        if subtitle_url.find('/'):
                            subtitle_filename = ((subtitle_url.rsplit('/', 1)[1]).lower())
                        my_logger.info("DLS - Downloading " + subtitle_filename + ".")
                        subtitle_download = requests.get(subtitle_url, allow_redirects=True)
                        open(process_directory + subtitle_filename, 'wb').write(subtitle_download.content)
                        new_subtitle_filename = re.sub(process_title, process_title.upper(), subtitle_filename, flags=re.IGNORECASE)
                        os.rename(process_directory + subtitle_filename, process_directory + new_subtitle_filename)
                        time.sleep(10)
            except:
                pass
    return process_subtitleavailable

def download_metadata(process_directory, process_cjson_directory, process_title, process_extension, process_subtitle_available):
    process_title = insert_hyphen_between_letters_and_numbers(process_title)
    metadata = javlibrary.get_video(process_title)
    if metadata is not None:
        metadata_array = { "Code": metadata.code, "Name": metadata.name, "Actress": metadata.actresses, "Studio": metadata.studio, "Image": metadata.image, "Genres": metadata.genres, "Score": metadata.score, "Location": process_directory + process_title + "/" + process_title + process_extension, "Subtitles": process_subtitle_available}
        metadata_json = json.dumps(metadata_array, indent=4)
        my_logger.info("GMD - Downloading metadata for " + process_title + ".json.")    
        with open(process_directory + process_title + "/" + process_title + ".json", "w") as outfile:
            outfile.write(metadata_json)
        with open(process_cjson_directory + process_title + ".json", "w") as outfile:
            outfile.write(metadata_json)
        # check if records exist
        # split out genre and actresses

        my_logger.info("GMD - Write metadata for " + process_title + " to database.")

        send_data_to_database(metadata, (process_directory + process_title + "/" + process_title + process_extension), (process_subtitle_available))
 
        # my_insert_sql_titles = "INSERT INTO titles (code, name, studio, image, score, location, subtitles) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY DO NOTHING"
        # my_insert_sql_genre = "INSERT INTO genre (code, description) VALUES (%s %s) ON DUPLICATE KEY UPDATE"
        # my_insert_sql_actresses = "INSERT INTO actresses (code, name) VALUES (%s %s) ON DUPLICATE KEY UPDATE"
                          
        #my_cursor.execute(my_insert_sql_titles, (metadata.code, metadata.name, metadata.studio, metadata.image, metadata.score, (process_directory + process_title + "/" + process_title + process_extension), (process_subtitle_available)))
        #my_cursor.execute(my_insert_sql_genre, (metadata.code, "xxx"))
        #my_cursor.execute(my_insert_sql_actresses, (metadata.code, "yyy"))

        


        #
        # Add 
        # To
        # Database
        #
        # Title
        # Actress
        # Genre
        # (date)
        #








    else:
        my_logger.info("GMD - No metadata for " + process_title + ".")

def send_data_to_database(process_metadata, process_location, process_subtitles_avail):
    my_insert_sql_titles = "INSERT IGNORE INTO titles (code, name, studio, image, score, location, subtitles) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    my_insert_sql_genre = "INSERT IGNORE INTO genre (code, description, key) VALUES (%s, %s, %s)"
    my_insert_sql_actresses = "INSERT IGNORE INTO actress (code, name, key) VALUES (%s, %s, %s)"

    my_cursor.execute(my_insert_sql_titles, (process_metadata.code, process_metadata.name, process_metadata.studio, process_metadata.image, process_metadata.score, process_location, process_subtitles_avail))

    # We need to avoid duplicates

    for g in process_metadata.genres:
        hash_input = (process_metadata.code + g).encode()
        hash_output = hashlib.md5(hash_input).hexdigest()
        print(hash_output)
        my_cursor.execute(my_insert_sql_genre, (process_metadata.code, g, hash_output))

    for a in process_metadata.actresses:
        hash_input = (process_metadata.code + a).encode()
        hash_output = hashlib.md5(hash_input).hexdigest()
        print(hash_output)
        my_cursor.execute(my_insert_sql_actresses, (process_metadata.code, a, hash_output))

    my_connection.commit()


def move_down_level(process_directory, process_file, process_extension):
    file_without_extension = re.sub(process_extension, '', process_file, flags=re.IGNORECASE)
    process_title = insert_hyphen_between_letters_and_numbers(file_without_extension)
    source_file = process_directory + process_title + "/" + process_title + process_extension
    destination_file = process_directory + process_title + process_extension
    if os.path.exists(source_file):
        my_logger.info("MDL - Moving " + source_file + " down-level.")
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
#    syslog_handler.setFormatter(logging.Formatter("RJMediaHasher %(message)s"))
#    return syslog_handler

def get_logger():
   logger = logging.getLogger()
   logger.setLevel(logging.INFO)
   logger.addHandler(get_console_handler())
   #logger.addHandler(get_syslog_handler())
   return logger

if __name__ == "__main__":
    # Define the directory you want to start the search + the file extension + language suffix
    base_directory = "/mnt/multimedia/Other/RatedFinalJ/Censored/10/"
    central_json_directory = "/mnt/multimedia/Other/RatedFinalJ/JSON/"
    target_extension = ".mp4"
    target_language = "en.srt"

    my_connection = mysql.connector.connect( 
        user="rjohnson", 
        password="5Nf%GB6r10bD", 
        host="diskstation.hachiko.int", 
        port=3306, 
        database="Test" 
    )
    
    my_cursor = my_connection.cursor()
    my_logger = get_logger()

    my_logger.info("======================================================================================")

    start_dir = os.listdir(base_directory)

    # Moves the files down level so they get rescanned.
    for file in start_dir:
        if os.path.isdir(base_directory + file):
            move_down_level(base_directory, file, target_extension)

    # # # # Do the scanning.
    for file in os.listdir(base_directory):
        if os.path.isfile(base_directory + file) and file.lower().endswith(target_extension):
            to_be_scraped = move_to_directory(base_directory, file, target_extension)
            subtitle_available = download_subtitlecat(base_directory, to_be_scraped, target_language)
            download_metadata(base_directory, central_json_directory, to_be_scraped, target_extension, subtitle_available)
            my_logger.info("======================================================================================")
            pass

    my_cursor.close()




    
