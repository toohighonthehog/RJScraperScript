import os, re, time
from javscraper import *
from module_rjscanfix import *

#title = "javme4lqz4"
title = "DASS-022"
#title = "042CLT-079"
#title = "abc123miad283af2ghj955docp094rr1qqq123x4rjrj65078dcx105"#
#title = "FC2-PPV-4289049"

f_my_javlibrary = JAVLibrary()
#print (f_my_javlibrary.search(title))
#print (f_my_javlibrary.get_video(title))
x, y = search_for_title(f_input_string = title, f_javli_override = "javme4lqz43")

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