import time
import sys
import notification
import extraction
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

user_input = sys.argv[1].replace(' ', '-').lower()
display_amount = int(sys.argv[2])

url = ("https://www.grailed.com/designers/" + user_input)

# 403 if no headers
hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

"""driver code (headless)"""
options = Options()
#options.add_argument("--headless")
driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.get(url)

# grailed needs time to populate items
time.sleep(3)

"""Sort popular by selecting element"""
try:
    select = Select(driver.find_element_by_id('Sort'))
    # print [o.text for o in select.options]
    select.select_by_index(4)
    print("\nSuccessfully Extracted Webpage!\n")
except:
    print("Connection Error!\n")
    exit(0)

print("Waiting 3 seconds for page to load\n")
time.sleep(3)

driver, display_amount = extraction.check_unlimited_scroll(display_amount, driver)

bs = Soup(driver.page_source, 'html.parser')

# find containers
containers = bs.find_all("div", class_="feed-item")

# initialize csv file with headers
try:
    filename = user_input + "-data.csv"
    f = open("data/" + filename, "w")
    headers = "product_id, brand, desc, size, original_price, new_price, price_change\n"
    f.write(headers)
except IOError:
    print "\nPermission Denied (File still open?)\n"
    exit(0)

print("\nSaving Results...\n")
extraction.save_results(containers, display_amount, user_input, f)

f.close()


