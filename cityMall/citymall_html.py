from bs4 import BeautifulSoup 
import requests

cityMall_url = "https://www.citymall.com.mm/citymall/en/Categories/Household-Essentials/Kitchen-Ware/Kitchen-Ware/Cooking-Utensil/Horseking-Food-Tong-9IN/p/cmhl_1000000317052_1"

response = requests.get(cityMall_url)

soup = BeautifulSoup(response.text, "html.parser")

script_tag = soup.find("script", id="text/javascript")

html = response.text

print(html)