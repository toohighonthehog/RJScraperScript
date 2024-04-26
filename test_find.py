#from ~/vscode/git/RJJAVScraperModule import javscraper
import javscraper, ast
import rjscanmodule.rjmetadata as rjmeta
import rjscanmodule.rjlogging as rjlog

#print (datetime.now())

# from module_rjscanfix import *deacr
#from rjscanmodule import *


#print (max((min(os.get_terminal_size().columns, 120),80)))

title = "javme4lqz4"
title = "SW-932"
title = "MIAD-283"
#title = "042CLT-079"
#title = "abc123miad283af2ghj955docp094rr1qqq123x4rjrj65078dcx105"#
#title = "FC2-PPV-4289049"

with open("cookie.json", "r") as data:
    cookie = ast.literal_eval(data.read())

my_javlibrary = javscraper.JAVLibrary()
my_javlibrary.debug = True
my_javlibrary._set_cookies(cookie)
my_logger = rjlog.get_logger()

print (my_javlibrary.search(title))
#print (f_my_javlibrary.get_video(title))
x, y = rjmeta.search_for_title(f_input_string = title)

metadata_array = rjmeta.download_metadata(
                        f_process_title=title,
                        f_my_logger=my_logger
)


print (f"{x} {y}")
print (metadata_array)

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