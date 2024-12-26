from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json

# Path to your ChromeDriver (adjust this to your local setup)
CHROME_DRIVER_PATH = 'C:/chromedriver/chromedriver-win64/chromedriver.exe'  # Make sure this path is correct

# Setup WebDriver using the Service object
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

BASE_URL = "https://www.citymall.com.mm/citymall/en"

# Search queries
search_queries = ["food", "drinks", "bulk", "milk", "noodles"]

# Function to scrape the search results page using Selenium
def scrape_search_page(query, page_number):
    search_url = f"{BASE_URL}/search/?text={query}&page={page_number}"
    print(f"Fetching: {search_url}")
    
    driver.get(search_url)  # Use driver.get(), which works with the updated WebDriver setup
    time.sleep(3)  # Give the page time to load (adjust as necessary)

    # Find all product items in the page
    product_listings = driver.find_elements(By.CSS_SELECTOR, 'div.col-xs-12.col-md-6.full-height')

    products = []
    for product in product_listings:
        # Extract product name and price
        try:
            product_name = product.find_element(By.CSS_SELECTOR, 'div.product-title')  # Adjust class if needed
            price = product.find_element(By.CSS_SELECTOR, 'div.product-price')  # Adjust class if needed

            if product_name and price:
                product_info = {
                    'product_name': product_name.text.strip(),
                    'price': price.text.strip(),
                }
                products.append(product_info)
        except Exception as e:
            print(f"Error extracting product info: {e}")

    return products

# Main function to start scraping
def main():
    all_products = []

    for query in search_queries:
        page_number = 1
        while True:
            products = scrape_search_page(query, page_number)
            if not products:  # No more products found
                break
            
            all_products.extend(products)
            page_number += 1  # Increment the page number to get the next page
            
            time.sleep(1)  # Sleep between requests to avoid being blocked

    # Save the data to a JSON file
    with open('citymall_products.json', 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)
    print(f"Scraping completed. Saved {len(all_products)} products to citymall_products.json")

if __name__ == "__main__":
    main()
