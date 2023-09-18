#import librairies
import os
from bs4 import BeautifulSoup as bs
import requests
import time

url="https://books.toscrape.com"

#Extraction des données du site avec boucle de test de connection au site while... response non ok pause
response= requests.get(url)
print(response.headers['content-type']) # 'text/html'
#print(response.encoding) # 'ISO-8859-1'

if response.ok:
    links=[]
    soup= bs(response.text, features="html.parser")
    title=soup.find("div", {"class": "col-sm-6 product_main"}).find("h1") # extrait le titre
    category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2] # recherche la catégorie
##    products=soup.findAll('<article class="product_pod">')
##    for product in products:
##        a=product.find('a')
##        link=a['href']
##        links.append(url+link)
    print(links)
    time.sleep(1)



liste_products=soup.findAll('All products')
print(liste_products)
def get_url(posi):
    pass
#Transformation en fichier csv

#Load
