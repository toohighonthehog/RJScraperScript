# from
# https://www.whatismybrowser.com/detect/what-is-my-user-agent/
# this cookie seems to last for only 30 mins

import javscraper, ast
from datetime import datetime

title = "MIAD-283"

# load the cookie
with open("cookie.json", "r") as data:
    cookie = ast.literal_eval(data.read())

#print (cookie)

f_my_javlibrary = javscraper.JAVLibrary()
f_my_javlibrary.debug = True
f_my_javlibrary._set_cookies(cookie)

# Show the time and run the check
print (datetime.now())
print (f_my_javlibrary.search(title))