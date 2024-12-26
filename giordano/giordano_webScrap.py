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
    Fetches product links for a given search query.
    """
    search_url = f"{BASE_URL}/search?type=product&q={query}"
    print(f"Searching for: {query} (URL: {search_url})")

    try:
        response = requests.get(search_url, headers=BASE_HEADERS, proxies=proxies, timeout=10)
        response.raise_for_status()
        print(f"Response Content-Type: {response.headers.get('Content-Type')}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to load search page for {query}. Error: {e}")
        return []

    # Check if the response content is binary
    if "text/html" not in response.headers.get("Content-Type", ""):
        print(f"Non-HTML content received for query '{query}'.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Save search page HTML for debugging
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
