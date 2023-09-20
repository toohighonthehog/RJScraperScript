import os, logging
import shutil
from RJFixIt import *

BASE_DIRECTORY = "/mnt/multimedia/Other/RatedFinalJ/Censored/12/"
TARGET_DIRECTORY = BASE_DIRECTORY
TARGET_EXENSIONS = [".mkv",".mp4",".avi"]
TARGET_LANGUAGE = "en.srt"

filename = "DOCP094A"
file_extension = ".mp4"

move_to_directory(BASE_DIRECTORY, TARGET_DIRECTORY, TARGET_LANGUAGE, filename, file_extension)