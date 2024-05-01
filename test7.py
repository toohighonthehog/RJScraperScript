import cloudscraper, ast

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
with open("cookie.json", "r") as data:
    cookie = ast.literal_eval(data.read())

SCRAPER = cloudscraper.create_scraper(
    # Make sure mobile pages are not served
    browser={
        "custom": USER_AGENT
    }
)

code = "IPZZ-002"
url = "https://www.javlibrary.com/en/?v=javmeear7a"
#url = "https://www.bbc.co.uk"

result = SCRAPER.get(
    url,
    allow_redirects=False,
    cookies=cookie,
    headers={}
    )

#print (result.text)

if code in result.text:
    print ("It's good")
else:
    print (result.status_code)


