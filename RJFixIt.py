import os, re, requests, json
from requests_html import HTMLSession
from javscraper import *
javlibrary = JAVLibrary()

# add a rerun option + re-get json
# and some logic to check we're not nesting deeper and deeper


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
    print(f"Moved :                 {process_file} to {destination_directory}")
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

    print(f"Process Directory :     {process_directory}")
    print(f"Process Title :         {process_title}")

    # Create the HTML session
    session = HTMLSession()
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
                        print(f"Subtitle_URL :          {subtitle_url}")
                        # Split out the filename
                        if subtitle_url.find('/'):
                            subtitle_filename = ((subtitle_url.rsplit('/', 1)[1]).lower())
                        print(f"Downloading :           '{subtitle_filename}'")
                        subtitle_download = requests.get(subtitle_url, allow_redirects=True)
                        open(process_directory + subtitle_filename, 'wb').write(subtitle_download.content)
                        new_subtitle_filename = re.sub(process_title, process_title.upper(), subtitle_filename, flags=re.IGNORECASE)
                        os.rename(process_directory + subtitle_filename, process_directory + new_subtitle_filename)
            except:
                pass




def download_metadata(process_directory, process_title):
    process_title = insert_hyphen_between_letters_and_numbers(process_title)
    metadata = javlibrary.get_video(process_title)
    if metadata is not None:
        metadata_array = { "Code": metadata.code, "Name": metadata.name, "Actresses": metadata.actresses, "Studio": metadata.studio, "Image": metadata.image, "Genres": metadata.genres, "Score": metadata.score}
        metadata_json = json.dumps(metadata_array, indent=4)
        print(f"Downloading Metadata :  {process_title}.json")    
        with open(process_directory + process_title + "/" + process_title + ".json", "w") as outfile:
            outfile.write(metadata_json)
    else:
        print(f"No Metadata for :       {process_title}")

def move_down_level(process_directory, process_file, process_extension):
    file_without_extension = re.sub(process_extension, '', process_file, flags=re.IGNORECASE)
    process_title = insert_hyphen_between_letters_and_numbers(file_without_extension)
    source_file = process_directory + process_title + "/" + process_title + process_extension
    destination_file = process_directory + process_title + process_extension
    if os.path.exists(source_file):
        #print(source_file)
        #print(destination_file)
        print(f"Moving Downlevel :       {source_file}")
        try:
            os.rename(source_file, destination_file)
        except:
            pass

if __name__ == "__main__":
    # Define the directory you want to start the search + the file extension + language suffix
    base_directory= "/mnt/multimedia/Other/RatedFinalJ/censored/12/"
    target_extension = ".mp4"
    target_language = "en.srt"

    print("============================================================================")

    start_dir = os.listdir(base_directory)

    # Moves the files down level so they get rescanned.
    for file in start_dir:
        if os.path.isdir(base_directory + file):
            move_down_level(base_directory, file, target_extension)

    # Do the scanning.
    for file in os.listdir(base_directory):
        if os.path.isfile(base_directory + file) and file.lower().endswith(target_extension):
            to_be_scraped = move_to_directory(base_directory, file, target_extension)
            print("----------------------------------------------------------------------------")
            download_subtitlecat(base_directory, to_be_scraped, target_language)
            print("----------------------------------------------------------------------------")
            download_metadata(base_directory, to_be_scraped)
            print("============================================================================")



    
