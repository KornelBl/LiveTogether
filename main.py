from bs4 import BeautifulSoup
import requests
import time
import webbrowser

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"


def otodom(soup: BeautifulSoup) -> str:
    h2 = soup.find(name="h2", attrs={"data-cy": "frontend.search.listing.title"})
    a = h2.find_next(name="a")
    return a["href"]


def olx(soup: BeautifulSoup) -> str:
    tab = soup.find(name="table", attrs={"id": "offers_table"})
    td = tab.find_next(name="tr", attrs={"class": "wrap"})
    a = td.find_next(name="a")
    return a["href"]


configs = {
    "otodom": {
        "base_url": "https://www.otodom.pl",
        "search_url": "https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/wroclaw/plac-grunwaldzki?distanceRadius=10"
                      "&market=ALL&page=1&limit=24&by=LATEST&direction=DESC&locations[0][regionId]=1&locations[0]["
                      "cityId]=39&locations[0][districtId]=26622&locations[0][subregionId]=381",
        "find_url": otodom,
        "last": ""
    },
    "olx": {
        "base_url": "",
        "search_url": "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/?search%5Bdist%5D=5&search"
                      "%5Bdistrict_id%5D=387",
        "find_url": olx,
        "last": ""
    }
}
chrome = webbrowser.get(chrome_path)
while True:
    for config in configs.values():
        page = requests.get(config["search_url"])
        text = page.text
        soup = BeautifulSoup(text, 'html.parser')
        a = config["find_url"](soup)
        newest_offer = config["base_url"] + a
        if config["last"] != newest_offer:
            config["last"] = newest_offer
            print(newest_offer)
            chrome.open(newest_offer)
    time.sleep(10)
