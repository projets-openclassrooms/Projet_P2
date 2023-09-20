import requests
from bs4 import BeautifulSoup

import csv

#fonction pour extraire (Extract) les informations d'un livre du site https://books.toscrape.com/
def get_book_info_from_url(link):
    response = requests.get(url)
    parse_url = BeautifulSoup(response.content, features='html.parser')
    return parse_url

#fonction pour transformer les données(Transform) à récupérer
def transform_book_info(parse_url):
    title = parse_url.h1.text.lower()
    upc = parse_url.select('#product_description ~ table td')[0].text
    title = parse_url.h1.text.lower()
    price_incl_tax = parse_url.select('#product_description ~ table td')[2].text
    price_excl_tax = parse_url.select('#product_description ~ table td')[3].text
    stock = parse_url.select('#product_description ~ table td')[5].text.replace('In stock (', '').replace('available)', '')
    description = parse_url.select("p")[3].text
    category = parse_url.select("a")[3].text
    review_rating = parse_url.find_all("p", class_="star-rating")[0].get("class")[1]
    image_url = main_url + parse_url.find("div", class_="item active").img["src"].replace('../', '')

#rubriques à recuperer sous forme de dictionnaire pour eviter les doublons plutot que listes
    return {
        'product_page_url': url,
        'universal_ product_code (upc)': upc,
        'title': title,
        'price_incl_tax': price_incl_tax,
        'price_excl_tax': price_excl_tax,
        'number_available': stock,
        'product_description': description,
        'category': category,
        'review_rating': review_rating,
        'image_url': image_url
    }

#fonction pour charger les données dans un fichier excel(Load), séparations : ','
def save_book_info_to_csv(book_info:dict):
    with open(
        'book_info.csv', 'w', encoding='utf-8-sig'
    ) as csvfile:
        writer = csv.DictWriter(csvfile, book_info, dialect='excel')
        writer.writeheader()
        #controle ligne vide pour ajout à la ligne suivante
        writer.writerow(book_info)

main_url = 'https://books.toscrape.com/'
#pour extraire une page test
url = main_url + "catalogue/dune-dune-1_151/index.html"

#pour extraire d'autres pages
url = main_url + "catalogue/its-only-the-himalayas_981/index.html"
#url = main_url + "catalogue/full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html"

if __name__ == '__main__':
    parse_url=get_book_info_from_url(url)
    save_book_info_to_csv(transform_book_info(parse_url))
