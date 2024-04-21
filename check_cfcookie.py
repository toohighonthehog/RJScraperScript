# from
# https://www.whatismybrowser.com/detect/what-is-my-user-agent/

import javscraper, ast
title = "MIAD-283"

#with open('cookie.json') as f: 
#    data = f.read()
#cookie = json.loads(data)

#cookie = {"cf_clearance": "wyE1.YAp9oCgn0U732aTjJOiQ_InFZ3ZT6PcIFrR_ic-1713696506-1.0.1.1-ivUGIH.zI_Fzt5hOjlTrWe4GyAmvecHkkmwsbM.._blOrQCBC2ysg1UXxtcoCREo_dli7TcxWpPJWQp3nPt32w"}
#print (cookie)
with open("cookie.json", "r") as data:
    cookie = ast.literal_eval(data.read())
print (cookie)
#cookie = json.loads(open("c.txt"))

#exit()

#print(type(cookie))

f_my_javlibrary = javscraper.JAVLibrary()
f_my_javlibrary.debug = True
f_my_javlibrary._set_cookies(cookie)
print (f_my_javlibrary.search(title))