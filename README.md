# Grailed Scraper

Python scraper to scrape Grailed based on popular designer products.

### Prequisites

requirements : 
* [Beautifulsoup4](https://pypi.org/project/beautifulsoup4/) - library to scrape information from web pages
```
pip install bs4
```

* [Selenium](https://www.seleniumhq.org/) - browser automation tool
```
pip install selenium
```

* [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) - automated testing with Google Chrome
#### chromedriver.exe must exist in same directory as import.py

### Usage

Specify which designer to scrape and how many items to scrape.

The resulting csv file will be saved in /data/
```
> python import.py "designer" [number of items to scrape]
```

Example:
```
> python import.py "common projects" 200
```


The above code will result in something similar to this:

![result](https://i.imgur.com/LtFOGH0.png)


 
