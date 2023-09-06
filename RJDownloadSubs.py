#apt install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
# https://stackoverflow.com/questions/67298635/request-html-render-working-on-windows-but-not-on-ubuntu

# sudo mount -t cifs -o username=xadmin //192.168.192.35/multimedia /mnt/multimedia

# pip install wget
# some checking if nothing is found.

# LFCSuperLouis15

from requests_html import HTMLSession
import re, os, requests

#clear the screen
os.system('clear')

# Create the session
session = HTMLSession()

# Define the URL and content
language="en.srt"
title = 'pred-505'
url = 'https://www.subtitlecat.com/index.php?search=' + title

try:
    os.mkdir(title)
except:
    pass

# Use the session to get the data
responselvl1 = session.get(url)

table = responselvl1.html.find('table')[0]
tabledata = [[c.absolute_links for c in row.find('td')][:1] for row in table.find('tr')][1:]

for tableentry in tabledata:
    fullurl = (list(tableentry[0])[0])
    if re.search(title, fullurl, re.IGNORECASE):
        responselvl2 = session.get(fullurl)
        subslist = responselvl2.html.xpath('/html/body/div[4]/div/div[2]', first=True)
        for suburl in subslist.absolute_links:
            if re.search(language, suburl, re.IGNORECASE):
                suburlresult = suburl
        try:
            if re.search(language, suburlresult, re.IGNORECASE):
                suburlresultcheck = (requests.head(suburlresult).status_code)
                if suburlresultcheck==200:
                    print(suburlresult)
                    # Split out the filename
                    if url.find('/'):
                        filename = ((suburlresult.rsplit('/', 1)[1]).lower())
                    print("Download " + filename)
                    rfile = requests.get(suburlresult, allow_redirects=True)
                    open(title + "/" + filename, 'wb').write(rfile.content)
                    print("======================================")
        except:
            pass







