import os, re, requests
from requests_html import HTMLSession

def move_to_folder(process_folder, process_extension):
    result = ""
    for file in os.listdir(process_folder):
        if os.path.isfile(process_folder + file) and file.endswith(process_extension):
            print(f"Moving : {file}")
            # Get the full path of the file
            #print(file + "xx")
            #file_path = os.path.join(root, file)
            # Extract the extension without the dot
            folder_without_dot = file.replace(process_extension,'')
            extension_without_dot = process_extension.strip(".")
            #print(folder_without_dot + "yy")

            # Create a folder with the same name as the extension if it doesn't exist
            destination_directory = process_folder + folder_without_dot

            print(destination_directory)

            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)

            # Move the file to the folder

            print(file)
            print(destination_directory)
            os.rename(start_directory + file, destination_directory + "/" + folder_without_dot + process_extension)
            print(f"Moved '{file}' to '{destination_directory}'")
            result = folder_without_dot
    
    return result

def insert_hyphen_between_letters_and_numbers(input_string):
    # Use regular expression to find all occurrences of letters followed by numbers
    # and insert a hyphen between them
    result = re.sub(r'([a-zA-Z])(\d)', r'\1-\2', input_string)
    return result

def download_subtitlecat(process_folder, process_title):
    
    process_folder = process_folder + process_title + "/"
    subfolder_title = process_title
    process_title = insert_hyphen_between_letters_and_numbers(title)


    print(process_folder)
    print(process_title)

    # Create the session
    session = HTMLSession()

    # Define the URL and content
    language="en.srt"
    url = 'https://www.subtitlecat.com/index.php?search=' + process_title

    # Use the session to get the data
    responselvl1 = session.get(url)

    table = responselvl1.html.find('table')[0]
    tabledata = [[c.absolute_links for c in row.find('td')][:1] for row in table.find('tr')][1:]

    for tableentry in tabledata:
        fullurl = (list(tableentry[0])[0])
        if re.search(process_title, fullurl, re.IGNORECASE):
            responselvl2 = session.get(fullurl)
            subslist = responselvl2.html.xpath('/html/body/div[4]/div/div[2]', first=True)
            for suburl in subslist.absolute_links:
                if re.search(language, suburl, re.IGNORECASE):
                    suburlresult = suburl
            try:
                if re.search(language, suburlresult, re.IGNORECASE):
                    suburlresultcheck = (requests.head(suburlresult).status_code)
                    if suburlresultcheck==200:
                        print(suburlresult)
                        # Split out the filename
                        if url.find('/'):
                            filename = ((suburlresult.rsplit('/', 1)[1]).lower())
                        print("Download " + filename)
                        rfile = requests.get(suburlresult, allow_redirects=True)
                        print(process_folder  + filename)
                        open(process_folder + filename, 'wb').write(rfile.content)
                        print("======================================")
            except:
                pass



#clear the screen
os.system('clear')

# Define the directory you want to start the search in
start_directory= "/mnt/multimedia/Other/RatedFinalJ/Censored/12/"
 
# Define the file extension you want to search for
target_extension = ".mp4"

# Define the URL and content
language="en.srt"

title = move_to_folder(start_directory, target_extension)

if len(title) > 0:
    download_subtitlecat(start_directory, title)


