import glob, os, re
from javscraper import *
my_javlibrary = JAVLibrary()

BASE_DIRECTORY = "/mnt/multimedia/Other/RatedFinalJ/Series/Bban/"
TARGET_EXTENSIONS = [".mkv", ".mp4", ".avi"]


# tidy up the variables a bit
def get_list_of_files():

        
    folder_list_1 = os.listdir(BASE_DIRECTORY)
    folder_list_2 = [file for file in folder_list_1 if any(file.endswith(ext) for ext in TARGET_EXTENSIONS)]
    folder_list_3 = []

    for file in folder_list_2:
        filename, file_extension = os.path.splitext(os.path.basename(file))
        if(my_javlibrary.search(filename)):
            folder_list_3.append(file)

    return folder_list_3

start_dir = os.listdir(BASE_DIRECTORY)
filterered_dir = get_list_of_files()




print(f"raw: {len(start_dir)}")
print(f"extra: {len(filterered_dir)}")
print(filterered_dir)


