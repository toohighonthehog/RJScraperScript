from module_rjscanfix import *
from javscraper import *
import re

count = 1
prefix = "HUNT"

p_my_javlibrary = JAVLibrary()

print (p_my_javlibrary.get_video("HUNT014"))
print (p_my_javlibrary.get_video("HUNT146"))
#print (p_my_javlibrary.get_video("MIAD283"))

# while count < 999:
#     count = count + 1
#     title = prefix + "{0:0=3d}".format(count)

#     try:
#         result = (p_my_javlibrary.get_video(title).name)
#     except:
#         pass
#     #print (result)
#     if re.search('model', result, re.IGNORECASE) or re.search('idol', result, re.IGNORECASE) or re.search('grav', result, re.IGNORECASE):
#         print (title)
#         print (result)

