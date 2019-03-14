from itertools import product
from bs4 import BeautifulSoup as Soup
import time
import re


def check_unlimited_scroll(display_amount, driver):
    item_count = 0
    loop_count = 0
    while item_count < display_amount:

        bs = Soup(driver.page_source, 'html.parser')
        item_count = len(bs.find_all("div", class_="feed-item"))

        loop_count = loop_count + 1

        print("Infinite Scroll Refresh iteration: " + str(loop_count) + " current item count: " + str(
            item_count) + " display amount: " + str(display_amount))

        page_length = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while match == False:
            last_count = page_length
            time.sleep(3)
            page_length = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if last_count == page_length:
                match = True
            break

    return driver


def extract_brand_name(container):
    brand_container = container.find_all("h3", class_="listing-designer")
    brand = brand_container[0].text.strip()
    brand = re.sub(r'[^a-zA-Z ]+', '', brand)
    return brand


def extract_product_id(container):
    product_id_container = container.find_all(class_="heart-follow")
    pid = product_id_container[0].get('id')
    pid = pid[2:]
    return pid


def extract_product_size(container):
    product_size_container = container.find_all("h3", class_="listing-size")
    ps = product_size_container[0].text.strip()
    return ps


"""removes brand name from desc"""


def extract_product_desc(container, user_input):
    product_desc_container = container.find_all("div", class_="truncate")
    pd = product_desc_container[0].text.strip()
    user_input = re.sub('-', ' ', user_input)
    for name in list(map(''.join, product(*(sorted({c.upper(), c.lower()} for c in user_input))))):
        pd = re.sub(name, '', pd)
    return pd


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


def calculate_price_reduction(old_price, new_price):
    old_price = re.sub(r'[^0-9]', '', old_price)
    new_price = re.sub(r'[^0-9]', '', new_price)
    percentage = round(((1 - (float(new_price) / float(old_price))) * 100), 2)
    percentage = str(percentage) + "%"
    return percentage


def save_results(containers, display_amount, user_input, f):
    item_number = 1
    for container in containers:

        product_id = extract_product_id(container)
        brand_name = extract_brand_name(container)
        product_size = extract_product_size(container)
        product_desc = extract_product_desc(container, user_input)
        original_price, new_price = extract_price(container)

        """handling price reduction"""
        if new_price == 0:
            # print("product ID: " + product_id + " item #: " + str(item_number) + "brand: " + brand_name + "  original price:" + str(original_price))

            f.write(
                product_id.encode("utf-8") + "," + brand_name.encode("utf-8") + "," + product_desc.encode(
                    "utf-8") + "," + product_size.encode("utf-8") + "," + original_price.replace(
                    ",", "").encode("utf-8") + "," + str(
                    "-") + "," + "" + "\n")

        else:
            # print("product ID: " + product_id + " item #: " + str(item_number) + "brand: " + brand_name + "  original price:" + str(original_price) + "  new price: " + str(new_price))
            price_change = calculate_price_reduction(original_price, new_price)

            f.write(
                product_id.encode("utf-8") + "," + brand_name.encode("utf-8") + "," + product_desc.encode(
                    "utf-8") + "," + product_size.encode("utf-8") + "," + original_price.replace(
                    ",",
                    "").encode("utf-8") + "," + new_price.replace(
                    ",", "").encode("utf-8") + "," + price_change + "\n")

        item_number = item_number + 1
        if item_number == display_amount: break
