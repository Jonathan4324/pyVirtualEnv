from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time

# Path to manually downloaded ChromeDriver
CHROME_DRIVER_PATH = "C:/chromedriver/chromedriver-win64/chromedriver.exe"

# Configure WebDriver
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

# Search queries
search_queries = ["food", "drinks", "bulk", "milk", "noodles"]

# Output CSV file
output_file = "citymall_products.csv"

# Write CSV headers
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Category", "Product ID", "Product Name", "Price", "Search Query"])

# Base URL for search
base_url = "https://www.citymall.com.mm/citymall/en/search/?text="

# Scraping process
try:
    for query in search_queries:
        search_url = f"{base_url}{query}"
        print(f"Scraping query: {query}")
        driver.get(search_url)
        time.sleep(5)  # Wait for page to load

        # Locate product elements
        products = driver.find_elements(By.CSS_SELECTOR, "div.product-tile")

        for product in products:
            try:
                # Extract product details
                category = product.find_element(By.CSS_SELECTOR, "div.category").text
                product_id = product.get_attribute("data-product-id")
                product_name = product.find_element(By.CSS_SELECTOR, "div.product-title").text
                price = product.find_element(By.CSS_SELECTOR, "div.price").text

                # Write to CSV
                with open(output_file, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([category, product_id, product_name, price, query])

            except Exception as e:
                print(f"Error extracting product: {e}")

finally:
    driver.quit()

print(f"Data saved to {output_file}.")
