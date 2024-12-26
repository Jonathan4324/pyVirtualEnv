import requests
from bs4 import BeautifulSoup
import json

# Base configuration
categories = [
    "https://giordanomm.com/collections/men-collections",
    "https://giordanomm.com/collections/women-collections",
    "https://giordanomm.com/collections/accessories-collection",
    "https://giordanomm.com/pages/active-fit-official-store",
    "https://giordanomm.com/collections/giordano-junior",
    "https://giordanomm.com/collections/giordano-travel-gear",
    "https://giordanomm.com/pages/bsx-official-store"
]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

# Function to scrape product data from JSON in script tag
def scrape_category_from_json(category_url):
    print(f"Processing category: {category_url}")
    response = requests.get(category_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to access: {category_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the script tag with type "application/json"
    script_tag = soup.find("script", type="application/json")
    if not script_tag:
        print(f"No JSON script tag found in: {category_url}")
        return []

    try:
        # Load the JSON data
        json_data = json.loads(script_tag.string)
        
        # Extract products (adjust keys based on the site's structure)
        products_data = json_data.get('products', [])
        products = []
        
        for product in products_data:
            name = product.get("name", "N/A")
            url = product.get("url", "N/A")
            image_url = product.get("images", [{}])[0].get("src", "N/A")
            price = product.get("price", "N/A")

            products.append({
                "name": name,
                "url": f"https://giordanomm.com{url}" if url != "N/A" else "N/A",
                "image_url": image_url,
                "price": price
            })

        print(f"Found {len(products)} products in: {category_url}")
        return products
    except Exception as e:
        print(f"Error parsing JSON data: {e}")
        return []

# Main script
all_products = []

for category in categories:
    category_products = scrape_category_from_json(category)
    all_products.extend(category_products)

# Save to JSON
output_file = "giordano_products.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(all_products, file, ensure_ascii=False, indent=4)

print(f"Scraping completed. {len(all_products)} products saved to {output_file}")
