from module_rjscanfix import *
from icecream import ic
import os, pathlib

SUBTITLE_WHISPER = "/mnt/multimedia/Other/~Miscellaneous/~SubtitleRepository/Whisper/"

my_connection = mysql.connector.connect( 
    user="rjohnson", 
    password="5Nf%GB6r10bD", 
    host="diskstation.hachiko.int", 
    port=3306, 
    database="Multimedia" 
)

def in_list(f_list, f_value):
    p_result = False
    for i in f_list:
        if f_value in i[0]:
            p_result = True

    return p_result

my_cursor = my_connection.cursor()

update_status = get_db_array(my_cursor)
#ic (update_status)

# ic (type(update_status))
# ic (type(update_status[0]))

filename = "CESD-773"

sub_record = (value_in_list(update_status, filename))
#ic (value_in_list(update_status, title)[1])
if ((sub_record[1]) == 5):
    source = (sub_record[2])# .replace('/mnt/', '/volume1/')
    destination = (SUBTITLE_WHISPER + "Audio/" + filename + ".mp3")# .replace('/mnt/', '/volume1/')
    print ("ffmpeg -i " + source + " " + destination)

    with open(SUBTITLE_WHISPER + "Audio/runner.sh", 'a') as f:
        f.write("ffmpeg -i " + source + " " + destination + "\n")
