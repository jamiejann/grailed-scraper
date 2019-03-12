import urllib2
import time
import re
import notification
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# user_input = raw_input("What brand are you looking for?\n").replace(' ', '-').lower()
# display_amount = raw_input("how many items?\n")
user_input = "chrome-hearts"
display_amount = 30

url = ("https://www.grailed.com/designers/" + user_input)

# 403 if no headers
hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

# driver code (headless)
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome('C:/Users/jami/Desktop/master/chromedriver.exe', options=options)
driver.get(url)

# grailed needs time to populate items
time.sleep(3)

bs = soup(driver.page_source, 'html.parser')

# find containers
containers = bs.find_all("div", class_="feed-item")


def extract_brand_name(container):
    brand_container = container.find_all("h3", class_="listing-designer")
    brand = brand_container[0].text.strip()
    brand = re.sub(r'[^a-zA-Z ]+', '', brand)
    return brand


def extract_product_id(container):
    product_id_container = container.find_all(class_="heart-follow")
    pid = product_id_container[0].get('id')
    return pid


def extract_product_size(container):
    product_size_container = container.find_all("h3", class_="listing-size")
    ps = product_size_container[0].text.strip()
    return ps


def extract_price(container):
    original_price_container = container.find_all("h3", class_="original-price")
    op = original_price_container[0].text.strip()

    if container.find_all("h3", class_="new-price"):
        new_price_container = container.find_all("h3", class_="new-price")
        np = new_price_container[0].text.strip()
        return op, np
    else:
        np = 0
        return op, np


# initialize csv file
filename = "file.csv"
f = open(filename, "w")
headers = "product_id, brand, size, original_price, new_price\n"
f.write(headers)

# extracting
item_number = 1
for container in containers:

    brand_name = extract_brand_name(container)
    product_id = extract_product_id(container)
    product_size = extract_product_size(container)
    original_price, new_price = extract_price(container)

    if new_price == 0:
        print("product ID: " + product_id + " item #: " + str(
            item_number) + "brand: " + brand_name + "  original price:" + str(original_price))

        f.write(product_id + "," + brand_name + "," + product_size + "," + original_price.replace(",", "") + "," + str(
            "-") + "\n")

    else:
        print("product ID: " + product_id + " item #: " + str(
            item_number) + "brand: " + brand_name + "  original price:" + str(original_price) + "  new price: " + str(
            new_price))

        f.write(product_id + "," + brand_name + "," + product_size + "," + original_price.replace(",",
                                                                                                  "") + "," + new_price.replace(
            ",", "") + "\n")

    item_number = item_number + 1
    if item_number == display_amount: break

f.close()
