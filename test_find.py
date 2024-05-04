#from ~/vscode/git/RJJAVScraperModule import javscraper
import javscraper, ast, os
import rjscanmodule.rjmetadata as rjmeta
import rjscanmodule.rjlogging as rjlog

#print (datetime.now())

# from module_rjscanfix import *deacr
#from rjscanmodule import *

os.system('cls' if os.name == 'nt' else 'clear')
#print (max((min(os.get_terminal_size().columns, 120),80)))

title = "SW-932"
#title = "IPZZ014" # javmeear7a
title = "DOCP-094"
#title = "042CLT-079"
title = "abc123miad283af2ghj955docp094rr1qqq123x4rjrj65078dcx105"#
title = "abc123miad283af2ghj955xocp094rr1qqq123x4rjrj65078xcx105"#
title = "hhd800.com@CAWD-675"
title = "abc123xiad283af2ghj955xocp094rr1qqq123x4rjrj65078xcx105"#
#title = "DOCP-094"

#title = "FC2-PPV-4289049"

with open("cookie.json", "r") as data:
    cookie = ast.literal_eval(data.read())

my_javlibrary = javscraper.JAVLibrary2() # do we need to use 2? is there a difference?
my_javlibrary.debug = False
my_javlibrary._set_cookies(cookie)
my_logger = rjlog.get_logger()

print (my_javlibrary.search("MIAD-283"))
#print (my_javlibrary.get_video(title))
#print (f_my_javlibrary.get_video(title))
x, y, z = rjmeta.new_search_title(f_input_string = title, f_my_logger = my_logger, f_attribute_override = None)

#metadata_array = rjmeta.download_metadata(
#                        f_process_title=title,
#                        f_my_logger=my_logger
#)


print (f"{x} {y}")
print (z)
#print (metadata_array)

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