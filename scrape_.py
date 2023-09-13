#import librairies
import os
from bs4 import BeautifulSoup as bs
import requests
import time

url="https://books.toscrape.com"

#Extraction des données
response= requests.get(url)
print(response.headers['content-type']) # 'text/html'
#print(response.encoding) # 'ISO-8859-1'

if response.ok:
    links=[]
    soup= bs(response.text, features="html.parser")
    products=soup.findAll('<article class="product_pod">')
    for product in products:
        a=product.find('a')
        link=a['href']
        links.append(url+link)
    print(links)
    time.sleep(1)



liste_products=soup.findAll('All products')
print(liste_products)
def get_url(posi):
    pass
#Transformation en fichier csv

#Load