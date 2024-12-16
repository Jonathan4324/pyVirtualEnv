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

print(product_info)