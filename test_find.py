from javscraper import *
import rjscanmodule.rjgeneral as rjgen
from datetime import datetime
import os

#print (datetime.now())

# from module_rjscanfix import *
#from rjscanmodule import *


#print (max((min(os.get_terminal_size().columns, 120),80)))

#title = "javme4lqz4"
title = "BBAN-022.gif"
#title = "042CLT-079"
#title = "abc123miad283af2ghj955docp094rr1qqq123x4rjrj65078dcx105"#
#title = "FC2-PPV-4289049"

f_my_javlibrary = JAVLibrary()
#print (f_my_javlibrary.search(title))
#print (f_my_javlibrary.get_video(title))
x, y = rjgen.search_for_title(f_input_string = title, f_javli_override = None)

#p_metadata = f_my_javlibrary.get_video("javme4lqz4")
#p_metadata_url = f_my_javlibrary.search("javme4lqz4")


print (f"{x} {y}")

#print (p_metadata)
#print (p_metadata_url)


#1 not null, count = 1
#    *get metadata, *scan for subs, *move

#2 not null, count = 0
#    blank metadata, *scan for subs, *move

#3 null, count != 1
#    just leave where it is




#12 get meta data
#1    real
#2    empty
#12 get subs
#12 write data + json
#12 move file
#3  do nothing