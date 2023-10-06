import re

import requests
from bs4 import BeautifulSoup as bs




# convertit le rating d'un str de lettres en int
def rating_to_int(rating):
    rating_map = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return rating_map.get(rating, rating)


def clean_name(name):
    cleaned_name = re.sub(r'[<>;:"/\\|?*]', "-", name)
    return cleaned_name


def download_img(img_url, name, category):
    if not os.path.exists("site_scraped"):
        os.makedirs("site_scraped")

    if not os.path.exists(f"site_scraped\{category}"):
        os.makedirs(f"site_scraped\{category}")

    name = clean_name(name)
    file_path = os.path.join("site_scraped", category, f"{name}.jpg")

    with open(file_path, "wb") as images:
        response = requests.get(img_url)

        if not response.ok:
            print(response)
        else:
            print("Téléchargement de l'image.", name)

        images.write(response.content)


# download_img('https://books.toscrape.com/catalogue/sharp-objects_997/index.html','Sharp Objects','mystery')

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

def pager(url):
    response = requests.get(url)

    # page = reponse.content  # créé une variable avec le contenu de cette réponse
    soup = bs(response.content, "html.parser")
    # si not pager
    #       i= 1
    #       si li class current de ul class pager = page 1 of 2
    #                                               resultat = nbrepages> 1
    #                                               for resultat:
    #                                                   recherche href et transform book info

    li_nexts = soup.find('form', class_="form-horizontal").text.strip().split()
    if int(li_nexts[0]) == 1:
        print(li_nexts[0], 'livre à récupérer.')
    else:
        print(li_nexts[0], 'livres à récupérer.')
    if li_nexts is not None:
        # next_page = li_nexts.find("strong")
        # print(next_page)
        pass


    else:
        print('nope!' * 3)

    if soup.find("ul", attrs="pager"):
        nb_pages = soup.find("ul", attrs="pager").text.strip().split()
        if nb_pages is not None:
            print(int(nb_pages[3]))
    else:
        print("nope")


def scrap_from_url(url, name):
    result = []  # init liste de la catégorie

    data = []  # init d'une liste d'1 livre

    reponse = requests.get(url)
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
    number_available = re.search(r"\d+", number_available).group()
    data.append(number_available)

    product_description = soup.find("meta", attrs={"name": "description"})
    product_description = product_description["content"].strip()
    data.append(product_description)

    category = soup.find(
        "a", href=re.compile(r"/category/books/([\w-]+)/index.html")
    ).string.strip()
    data.append(category)

    review_rating = soup.find("p", class_=re.compile(r"star-rating\s+(\w+)"))
    review_rating = re.search(r"\b(\w+)\b", review_rating["class"][1]).group(1)
    review_rating = review_rating.strip()
    review_rating = rating_to_int(review_rating)
    data.append(review_rating)

    image_url = soup.find("img")["src"]
    image_url = image_url.replace("../", "")  # on retire les ../../ au début du lien
    image_url = "https://books.toscrape.com/" + image_url
    data.append(image_url)

    download_img(image_url, title, name)

    result.append(data)
    return result


# def get_all_pages(liens):
#     url_liens = liens
#     urls = []
#     categories = []
#     url_liens_temp = url_liens
#     print(url_liens_temp, url_liens)
#     while True:
#         reponse = requests.get(url_liens)
#         page = reponse.content
#         soup = bs(page, "html.parser")
#         urls.append(url_liens)
#         li_nexts = soup.find_all("li", class_="next")
#         if li_nexts is not None:
#             next_page = li_nexts.find("a")
#             # print(li_nexts)
#
#             if next_page is not None:
#                 url_liens = next_page["href"]
#
#                 url_liens = url_liens_temp + url_liens
#                 # print(url_liens)
#             else:
#                 break
#         else:
#             break
#
#         for url in urls:
#             reponse = requests.get(url)
#
#             page = reponse.content
#             soup = bs(page, "html.parser")
#
#             h3_tags = soup.find_all("h3")
#             # récupère les balises h3 contenant les urls des livres
#             # retire les ../../ en début d'url
#             # retourne une liste complete d'url
#             for h3_tag in h3_tags:
#                 link_tag = h3_tag.a
#                 href_value = link_tag["href"].replace("../", "")
#                 href_value = f"{home_url}catalogue/{href_value}"
#                 categories.append(href_value)
#
#     return categories


def get_cat_liens(url):
    # recuperation sous forme de liste les liens url / categories à selectionner
    # selection des noms des categories 'name_categories'
    reponse = requests.get(url)

    # page = reponse.content  # créé une variable avec le contenu de cette réponse
    soup = bs(reponse.content, "html.parser")
    datas = []  # initialisation de la liste qui stocke les urls
    # name_categories = [] # initialisation des noms des categories

    for i in range(51):
        name_cat = soup.find("ul", class_="nav nav-list").find_all("li")[i].get_text(strip=True)

        all_cat = soup.find("ul", class_="nav nav-list").findAll('a')[i]['href'][:]
        # name_categories.append(name_cat)

        # datas.append(all_cat)
        dict_categories = {'name': name_cat, 'url_cat': all_cat}
        datas.append(dict_categories)

    datas.pop(0)
    # name_categories.pop(0)

    return datas


"""
# to run the script. 
"""


def scrap_category(choix):
    print(choix)
    pager(choix)
    print()
