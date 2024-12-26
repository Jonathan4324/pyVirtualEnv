import requests
from bs4 import BeautifulSoup
import json

# Base configuration
categories = [
    "https://sisburma.com/product-category/uncategorized/",
    "https://sisburma.com/product-category/outerwear/",
    "https://sisburma.com/product-category/new-products/",
    "https://sisburma.com/product-category/100-cotton/",
    "https://sisburma.com/product-category/accessories/",
    "https://sisburma.com/product-category/arcader-collection/",
    "https://sisburma.com/product-category/men/",
    "https://sisburma.com/product-category/pants/",
    "https://sisburma.com/product-category/series/",
    "https://sisburma.com/product-category/topwear/",
    "https://sisburma.com/product-category/underwear/"
]
headers = {"User-Agent": "Mozilla/5.0"}

# Function to scrape products from a category
def scrape_category(category_url):
    print(f"Processing category: {category_url}")
    response = requests.get(category_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to access: {category_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # WooCommerce product container class (inspect to confirm)
    product_containers = soup.find_all("li", class_="product")  # Adjust 'product' class if needed
    products = []

    for product in product_containers:
        try:
            # Extract product name
            name = product.find("h2").text.strip() if product.find("h2") else "N/A"

            # Extract product URL
            link = product.find("a")["href"] if product.find("a") else "N/A"

            # Extract product image URL
            img_tag = product.find("img")
            image_url = img_tag["src"] if img_tag else "N/A"

            # Extract product price
            price_tag = product.find("span", class_="woocommerce-Price-amount")
            price = price_tag.text.strip() if price_tag else "N/A"

            # Append product info
            products.append({
                "name": name,
                "url": link,
                "image_url": image_url,
                "price": price
            })
        except Exception as e:
            print(f"Error extracting product: {e}")

    print(f"Found {len(products)} products in: {category_url}")
    return products

# Main script
all_products = []

for category in categories:
    category_products = scrape_category(category)
    all_products.extend(category_products)

# Save to JSON
output_file = "sisburma_product_data.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(all_products, file, ensure_ascii=False, indent=4)

print(f"Data scraping completed. {len(all_products)} products saved to {output_file}")
