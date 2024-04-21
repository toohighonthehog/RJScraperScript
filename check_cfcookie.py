# from
# https://www.whatismybrowser.com/detect/what-is-my-user-agent/
# this cookie seems to last for only 30 mins

import javscraper, ast, os
from datetime import datetime
import rjscanmodule.rjlogging as rjlog

os.system("clear")
title = "MIAD-283"

# load the cookie
with open("cookie.json", "r") as data:
    cookie = ast.literal_eval(data.read())

#print (cookie)

my_javlibrary = javscraper.JAVLibrary()
my_javlibrary.debug = True
my_javlibrary._set_cookies(cookie)
my_logger = rjlog.get_logger()

# Show the time and run the check
while True:
    print (datetime.now())
    result = my_javlibrary.search(title)
    my_logger.info(rjlog.logt(f"{result}."))
    sleep 30