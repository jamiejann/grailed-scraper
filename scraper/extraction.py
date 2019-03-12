import re


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


def save_results(containers, display_amount, f):
    item_number = 1
    for container in containers:

        brand_name = extract_brand_name(container)
        product_id = extract_product_id(container)
        product_size = extract_product_size(container)
        original_price, new_price = extract_price(container)

        """handling price reduction"""
        if new_price == 0:
            print("product ID: " + product_id + " item #: " + str(
                item_number) + "brand: " + brand_name + "  original price:" + str(original_price))

            f.write(
                product_id + "," + brand_name + "," + product_size + "," + original_price.replace(",", "") + "," + str("-") + "\n")

        else:
            print("product ID: " + product_id + " item #: " + str(
                item_number) + "brand: " + brand_name + "  original price:" + str(
                original_price) + "  new price: " + str(
                new_price))

            f.write(product_id + "," + brand_name + "," + product_size + "," + original_price.replace(",", "") + "," + new_price.replace(",", "") + "\n")

        item_number = item_number + 1
        if item_number == display_amount: break
