import re

import requests
from bs4 import BeautifulSoup as bs
from scrape_images import download_img


# convertit le rating d'un str de lettres en int
def rating_to_int(rating):
    rating_map = {
        "Zero": 0,
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5}
    return rating_map.get(rating, rating)


# extrait les informations de livres d'une catégorie depuis liens urls :
# - product_page_url
# - universal_ product_code (upc)
# - title
# - price_including_tax
# - price_excluding_tax
# - number_available
# - product_description
# - category
# - review_rating
# - image_url
# resultat sous forme de liste

def scrap_from_url(urls, name):
    result = []  # init liste de la catégorie
    for url in urls:
        data = []  # init d'une liste d'1 livre

        try:  # gestion des erreurs dans la requete
            reponse = requests.get(url)
        except requests.exceptions.RequestException as erreur:
            print(erreur)
        page = reponse.content


        soup = bs(page, "html.parser")


        product_page_url = url
        data.append(product_page_url)

        upc = soup.find("th", string="UPC")
        upc = upc.find_next("td").string.strip()
        data.append(upc)

        title = soup.find("h1").text.strip()
        data.append(title)

        # même principe que pour l'UPC
        price_including_tax = soup.find("th", string="Price (incl. tax)")
        price_including_tax = price_including_tax.find_next("td").string.strip()
        data.append(price_including_tax)

        # même principe que pour l'UPC
        price_excluding_tax = soup.find("th", string="Price (excl. tax)")
        price_excluding_tax = price_excluding_tax.find_next("td").string.strip()
        data.append(price_excluding_tax)

        # même principe que pour l'UPC
        number_available = soup.find("th", string="Availability")
        number_available = number_available.find_next("td").string.strip()
        number_available = re.search(r'\d+', number_available).group()
        data.append(number_available)

        product_description = soup.find("meta", attrs={"name": "description"})
        product_description = product_description["content"].strip()
        data.append(product_description)

        category = soup.find("a", href=re.compile(
            r'/category/books/([\w-]+)/index.html')).string.strip()
        data.append(category)

        review_rating = soup.find("p", class_=re.compile(r'star-rating\s+(\w+)'))
        review_rating = re.search(r'\b(\w+)\b', review_rating["class"][1]).group(1)
        review_rating = review_rating.strip()
        review_rating = rating_to_int(review_rating)
        data.append(review_rating)

        image_url = soup.find("img")["src"]
        image_url = image_url.replace("../", "")  # on retire les ../../ au début du lien
        image_url = "http://books.toscrape.com/" + image_url
        data.append(image_url)

        download_img(image_url, title, name)

        result.append(data)
    return result
