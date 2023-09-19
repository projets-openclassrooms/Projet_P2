#import librairies
import os
from bs4 import BeautifulSoup as bs
import requests
import time

trait="-"*100

#url du site
url = "https://books.toscrape.com"

#url pour extraire les donnees de la page "travel" pour test
url = url + "/catalogue/dune-dune-1_151/index.html"

#Extraction des données du site avec test de connection au site, response non ok pause
response= requests.get(url, timeout= 1)
print(trait)

if response.status_code == requests.codes.ok:
    print(response.headers['content-type']) # 'text/html'

if response.encoding == 'ISO-8859-1':
    response.encoding='utf-8'
    print(response.encoding)

if response.ok:
    links=[]
    soup= bs(response.content, features="html.parser")
    # soup.prettify() pour connaitre la structure de la page html
    #print(soup.prettify())
    title = soup.h1.text.lower()
    price = soup.select('#product_description ~ table td')[3].text
    print(title, price)
