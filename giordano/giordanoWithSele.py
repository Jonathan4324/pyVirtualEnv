from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# Proxy credentials
host = 'brd.superproxy.io'
port = 33335
username = os.getenv('Bright_Data_username')
password = os.getenv('Bright_Data_pwd')

# Proxy URL and setup
proxy_url = f'http://{username}:{password}@{host}:{port}'
proxies = {
    'http': proxy_url,
    'https': proxy_url
}

CHROME_DRIVER_PATH = 'C:/chromedriver/chromedriver-win64/chromedriver.exe'  # chrome web driver path
# Set up Selenium with headless mode
chrome_options = Options()
# Remove headless argument for debugging
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(f"--proxy-server={proxy_url}")

# Setup WebDriver using the Service object
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Base URLs and constants
BASE_URL = "https://giordanomm.com"
SEARCH_QUERIES = ["pants", "cloth", "men", "women", "popular", "best", "season"]
OUTPUT_FILE = "giordano_products.json"

# Standard headers for requests
BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}


def get_search_results(query):
    """
    Fetches product links for a given search query using Selenium.
    """
    search_url = f"{BASE_URL}/search?type=product&q={query}"
    print(f"Searching for: {query} (URL: {search_url})")

    try:
        driver.get(search_url)
        print("Page loaded. Title:", driver.title)

        # Save search page HTML for debugging
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        with open("search_page_debug.html", "w", encoding="utf-8") as debug_file:
            debug_file.write(soup.prettify())

        # Extract product links
        product_links = []
        product_divs = soup.find_all('div', class_="product-template product-template-default")
        if not product_divs:
            print(f"No product divs found for query '{query}'. Check the structure of the page.")
            return []

        for product_div in product_divs:
            link_tag = product_div.find('a', href=True)
            if link_tag:
                product_links.append(BASE_URL + link_tag['href'])

        print(f"Found {len(product_links)} product links for query '{query}': {product_links}")
        return product_links

    except Exception as e:
        print(f"Error while processing query '{query}': {e}")
        return []
    # Commenting out the finally block to debug the issue
    # finally:
    #     input("Press Enter to close the browser...")  # Keep the browser open for inspection
