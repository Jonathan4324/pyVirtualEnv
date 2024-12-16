from bs4 import BeautifulSoup
import requests

walmart_url = "https://www.walmart.com/ip/onn-34-Curved-Ultrawide-WQHD-3440-x-1440p-100Hz-Bezel-Less-Office-Monitor-with-Cable-Black/2522348721"

response = requests.get(walmart_url)

html = response.text

print(html)