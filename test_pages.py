import re
import os
from pathlib import Path
import requests
import slugify
from bs4 import BeautifulSoup as bts

home_url = "https://books.toscrape.com/"
page = "https://books.toscrape.com/catalogue/page"
i= 1
catalogue = page + "{}_html".format(i)

print(catalogue.format(2))