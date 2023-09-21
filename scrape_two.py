#import des librairies
import requests
from bs4 import BeautifulSoup
from scrape_one import get_book_info_from_url

#variables pour lister urls, liste des categories
urls = []
data = []
categories= []

#fonction parser categories
#
def transform_book_categories(parse_url):
    # parser liens des categories

    for category in parse_url.css('.nav nav-list'):
      bloc_categories = yield {'category': category.css('::text').get()}

    return bloc_categories
def categories_to_list(nom):
    #creer liste des categories
    categories = parse_url.find(class_="nav-list")
    all_hrefs = [a.get('href') for a in categories.find_all('a')]


    [category.append() for category in categories]

#process pour tester foncctions
url = 'https://books.toscrape.com/'
categories_url=get_book_info_from_url(url)
print(transform_book_categories(categories_url)) #find("div", class_="side_categories", class_="nav-list")

response = requests.get(url)
print(response)
parse_url = BeautifulSoup(response.content, features='html.parser')

print(parse_url.title.string) #titre

nblinks =len( parse_url.get_text('catalogue/category'))
print(nblinks) # nombre <> 50 pas la bonne commande
categories= parse_url.find(class_="nav-list")
all_hrefs = [a.get('href') for a in categories.find_all('a')]
print(all_hrefs)