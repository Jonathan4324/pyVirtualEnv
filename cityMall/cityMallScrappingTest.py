import requests
from bs4 import BeautifulSoup
import json
import queue

import time

#import pprint
import requests

import os
from requests.exceptions import ProxyError, HTTPError
from dotenv import load_dotenv

load_dotenv()

host = 'brd.superproxy.io'
port = 33335

username = os.environ['Bright_Data_username']
password = os.environ['Bright_Data_pwd']

proxy_url = f'http://{username}:{password}@{host}:{port}'

proxies = {
    'http': proxy_url,
    'https': proxy_url
}

 ## This is example code request 
# url = "http://lumtest.com/myip.json"
# response = requests.get(url, proxies=proxies)
# pprint.pprint(response.json())



BASE_URL = "https://www.citymall.com.mm/citymall/en/"
OUTPUT_FILE = "cityMall_product_info.jsonlinkNewOne"

# Fake browser-like headers
BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    #"accept": "text/html, application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng, */*;q=0.8",
    "accept": "application/json",
    "accept-language": "en-US",
    "accept-encoding": "gzip, deflate, br, zstd",
}

# List of search queries
search_queries = ["bulk+products", "Beverages", "Dairy,Bakery & Frozen Food"]


# Initialize a queue for product URLs and a set for seen URLs
product_queue = queue.Queue()
seen_urls = set()


#https://www.citymall.com.mm/citymall/en/search?q=bulk+products%3Arelevance&page=0

#https://www.citymall.com.mm/citymall/en/search?q=bulk+products%1Arelevance&page=0
def get_product_links_from_search_page(query, page_number, page_minus):
    search_url = f"https://www.citymall.com.mm/citymall/en/search?q={query}%{page_number}Arelevance&page={page_minus}"
    max_retries = 5
    backoff_factor = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(search_url, headers=BASE_HEADERS, proxies=proxies)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            product_links = []

            found = False
            for a_tag in soup.find_all('a', href=True):
                if '/ip/' in a_tag['href']:
                    found = True
                    if "https" in a_tag['href']:
                        full_url = a_tag['href']
                    else:
                        full_url = BASE_URL + a_tag['href']

                    if full_url not in seen_urls:
                        product_links.append(full_url)

            if not found:
                print("\n\n\nSOUP WHEN NOT FOUND", soup)

            return product_links

        except ProxyError as e:
            wait_time = backoff_factor ** attempt
            print(f"Proxy error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except HTTPError as e:
            if e.response.status_code == 412:
                print(f"Precondition Failed (412): {e}. Skipping URL.")
                break
            wait_time = backoff_factor ** attempt
            print(f"HTTP error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Failed to get product links for query: {query} on page: {page_number}. Error: {e}")
            break

    print(f"Skipping query after {max_retries} retries: {query} on page: {page_number}")
    return []



def extract_product_info(product_url):
    print("Processing URL", product_url)
    max_retries = 5
    backoff_factor = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(product_url, headers=BASE_HEADERS, proxies=proxies)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', id='__NEXT_DATA__')

            if script_tag is None:
                return None

            data = json.loads(script_tag.string)
            initial_data = data["props"]["pageProps"]["initialData"]["data"]
            product_data = initial_data["product"]
            reviews_data = initial_data.get("reviews", {})

            product_info = {
                "price": product_data["priceInfo"]["currentPrice"]["price"],
                "review_count": reviews_data.get("totalReviewCount", 0),
                "item_id": product_data["usItemId"],
                "avg_rating": reviews_data.get("averageOverallRating", 0),
                "product_name": product_data["name"],
                "brand": product_data.get("brand", ""),
                "availability": product_data["availabilityStatus"],
                "image_url": product_data["imageInfo"]["thumbnailUrl"],
                "short_description": product_data.get("shortDescription", "")
            }

            return product_info

        except ProxyError as e:
            wait_time = backoff_factor ** attempt
            print(f"Proxy error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except HTTPError as e:
            if e.response.status_code == 412:
                print(f"Precondition Failed (412): {e}. Skipping URL.")
                break
            wait_time = backoff_factor ** attempt
            print(f"HTTP error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Failed to process URL: {product_url}. Error: {e}")
            break

    print(f"Skipping URL after {max_retries} retries: {product_url}")
    return None



def main():
    with open(OUTPUT_FILE, 'w') as file:
        while search_queries:
            current_query = search_queries.pop(0)
            print("\n\nCURRENT QUERY", current_query, "\n\n")
            page_number = 1
            page_minus = 0

            while True:
                product_links = get_product_links_from_search_page(current_query, page_number, page_minus)
                if not product_links or page_number or page_minus > 99:
                    break

                for link in product_links:
                    if link not in seen_urls:
                        product_queue.put(link)
                        seen_urls.add(link)

                while not product_queue.empty():
                    product_url = product_queue.get()
                    product_info = extract_product_info(product_url)
                    if product_info:
                        file.write(json.dumps(product_info) + "\n")

                page_number += 1
                page_minus +=0
                print(page_number, page_minus)

if __name__ == "__main__":
    main()