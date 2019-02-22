#from urllib2 import urlopen as uReq
import urllib2
import time
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'http://www.grailed.com/shop/chrome-hearts'

#403 if no headers
hdr = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome('/mnt/c/Users/jami/Desktop/master/chromedriver.exe', options = options) 

driver.get(url)

#grailed needs time to populate items
time.sleep(3)

bs = soup(driver.page_source, 'html.parser')

#find containers
containers = bs.find_all("div", class_="feed-item")
