from bs4 import BeautifulSoup
import requests
import json

walmart_url = "https://www.walmart.com/ip/onn-34-Curved-Ultrawide-WQHD-3440-x-1440p-100Hz-Bezel-Less-Office-Monitor-with-Cable-Black/2522348721"

HEADERS = {
    "Accept" : "*/*",
    "Accept-Encoding" : "gzip, deflate, br, zstd",
    "Accept-Language" : "en-US,en;q=0.9",
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}

response = requests.get(walmart_url, headers=HEADERS)

soup = BeautifulSoup(response.text, "html.parser")

script_tag = soup.find("script", id="__NEXT_DATA__")

data = json.loads(script_tag.string)

print(data['props']['pageProps']['initialData']['data']['product']['priceInfo']['currentPrice']['price'])