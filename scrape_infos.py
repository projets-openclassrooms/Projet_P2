import re

import requests
import slugify
from bs4 import BeautifulSoup as bs
from math import ceil

# convertit le rating d'un str de lettres en int
def rating_to_int(rating):
    rating_map = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return rating_map.get(rating, rating)


def clean_name(name):
    re.sub(r'[^\x00-\x7F]','-',name)
    cleaned_name = slugify(text)
    return cleaned_name

def nb_of_pages(link):
    """
    Si plus de 20 / pages alors
    valeur entiere + 1 pour avoir page_1
.   et non pas page_0
    """
    nb_pages = []
    page = requests.get(link)
    soup = bs(page.text, "html.parser")
    nb_links = int(soup.find_all("strong")[1].text)
    nb_pages = ceil(nb_links/20)
    print(type(nb_pages))
    if int(nb_pages) ==0:
        nb_pages += 1
    else:
        nb_pages
    return nb_pages
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
        nblivres = int(li_nexts[0])
        return nblivres
    if li_nexts is not None:
        # next_page = li_nexts.find("strong")
        # print(next_page)
        pass


    else:
        print('nope!' * 3)

    if soup.find("ul", attrs="pager"):
        nb_pages = soup.find("ul", attrs="pager").text.strip().split()
        nb_pages_int = int(nb_pages[3])
        if nb_pages is not None:
            return nb_pages_int

    else:
        nb_pages_int = 1
        return nb_pages_int


def get_book_info_from_url(liens):
    response = requests.get(liens)
    parse_url = bs(response.content, features='html.parser')
    print(parse_url.prettify())
    return parse_url


def contenu_livres(parse_url):
    result = []  # init liste de la catégorie

    data = []  # init d'une liste d'1 livre
    print(parse_url)


    title = parse_url.h1.text.lower()
    #title = clean_name(title)

    upc = parse_url.select('#product_description ~ table td')[0].text
    #upc = parse_url.h2.find("th","UPC").find_next_siblings().text
    #upc = clean_name(upc)
    #title = parse_url.h1.text.lower()
    #title = clean_name(title)
    price_incl_tax = parse_url.select('#product_description ~ table td')[2].text
    price_excl_tax = parse_url.select('#product_description ~ table td')[3].text
    #stock = parse_url.select('#product_description ~ table td')[5].text.replace('In stock (', '').replace('available)',
    #                                                                                                      '')
    # description remplie d'espace au lieu du vide, nettoyee de ; pour eviter decalage colonne
#     < div id = "product_description" class ="sub-header" >
#     < h2 > Product  Description < / h2 >
#       < / div >
#       < p > bla bla...
    #description = parse_url.select("p")[3].text
    stock = soup.find(
        class_="instock availability"
    ).text.strip()
    stock = "".join(i for i in number_available if i.isdigit())
    description = soup.head.find(
        "meta", attrs={"name": "description"}
    )
    product_description = description.attrs["content"].strip()
    if description:
        description = description.replace(';', ',')
    else:
        description = " " # si description vide

    category = parse_url.select("a")[3].text
    # review_rating convertie en valeur entiere et non info
    review_rating = parse_url.find_all("p", class_="star-rating")[0].get("class")[1]
    #si review rating vide
    if review_rating is not None:
        review_rating = rating_to_int(review_rating)
    else:
        review_rating = int(0)

    image_url = url + parse_url.find("div", class_="item active").img["src"].replace('../', '')
    # rubriques à recuperer sous forme de dictionnaire pour eviter les doublons plutot que listes
    book_datas = {
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
    return book_datas


def get_all_pages(liens):
    url_liens = liens
    urls = []
    categories = []
    url_liens_temp = url_liens
    print(url_liens_temp, url_liens)
    while True:
        reponse = requests.get(url_liens)
        page = reponse.content
        soup = bs(page, "html.parser")
        urls.append(url_liens)
        li_nexts = soup.find_all("li", class_="next")
        if li_nexts is not None:
            next_page = li_nexts.find("a")
            # print(li_nexts)

            if next_page is not None:
                url_liens = next_page["href"]

                url_liens = url_liens_temp + url_liens
                # print(url_liens)
            else:
                break
        else:
            break

        for url in urls:
            reponse = requests.get(url)

            page = reponse.content
            soup = bs(page, "html.parser")

            h3_tags = soup.find_all("h3")
            # récupère les balises h3 contenant les urls des livres
            # retire les ../../ en début d'url
            # retourne une liste complete d'url
            for h3_tag in h3_tags:
                link_tag = h3_tag.a
                href_value = link_tag["href"].replace("../", "")
                href_value = f"{home_url}catalogue/{href_value}"
                categories.append(href_value)

    return categories


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
#url = "https://books.toscrape.com/catalogue/the-long-shadow-of-small-ghosts-murder-and-memory-in-an-american-city_848/index.html"


def scrap_category(choix):
    #print(choix)

    req = requests.get(choix)
    soup = bs(req.content, 'lxml')
    books_tag = soup.find_all('div', class_ = 'image_container')
    print (len(books_tag))
    prod = soup.find_all(class_="product_pod")[0].find("a").attrs["href"]
    # get_all_pages(choix)
    for x in href_category[1:]:

        Category = x.string
        Category = Category.replace("\n", "").strip()
        href = x["href"]
        hreflink = 'http://books.toscrape.com/' + href
        print(hreflink)
        for j in range(1, 9):
            if j == 1:
                pass
            if j == 2:
                page_number = f"page-{j}.html"
                hreflink = hreflink.replace("index.html", page_number)
            if j > 2:
                page_number = f"page-{j}.html"
                hreflink = hreflink.replace(f"page-{j - 1}.html", page_number)

            response = requests.get(hreflink)
            if response.status_code == 200:
                print(f">scrape link : {hreflink}")

                soup = bs(response.text, "html.parser")
                section = soup.find('section')
                list_ordonnee = section.find('ol')
                article = list_ordonnee.find_all('article', attrs={"class": 'product_pod'})

                for i in article:
                    Data = {}
                    h3 = i.find('h3')
                    a = h3.find('a')
                    href = a.attrs['href']
                    href = "http://books.toscrape.com/catalogue" + href[8:]
                    response = requests.get(href)
                    print(f">>scrape book : {href}")
                    soupart = bs(response.text, "html.parser")
                    title = soupart.find('h1')

                    Data["Genre"] = Category
                    Data["Title"] = title.string
                    price = soupart.find('p', attrs={'class': 'price_color'})
                    price = price.text
                    Data["price"] = price[2:]
                    instock = soupart.find("p", class_="instock availability")
                    instock = instock.text.strip()
                    Data["Stock"] = instock[10:12]
                    stars = soupart.find("p", class_="star-rating")
                    stars = stars['class']
                    stars = stars[1]
                    Data["Star"] = stars_rate[stars]

                    Table = soupart.find("table")
                    UPC = Table.find_all('td')[0]
                    UPC = UPC.string
                    Data["UPC"] = UPC
                    Type = Table.find_all('td')[1]
                    Data["Type"] = Type.text
                    Tax = Table.find_all('td')[4]
                    Tax = Tax.text
                    Data["Tax"] = Tax[2:]
                    Number_of_reviews = Table.find_all('td')[-1]
                    Data["Number of reviews"] = Number_of_reviews.text
                    des = soupart.find_all('p')
                    des = des[3]
                    des = des.text
                    des = " ".join(des.split(",")[:3]) + "||Fore More You should read this books. Thanks"
                    Data["desc"] = des
                    l.append(Data)
            else:
                print(f"not found : ?? page number{j}")

    # for pro in prod:
    #     #print(prod)
    # books = []
    # for i in range(len(prod)):
    #     #books_link = soup.find.a['href']
    #     ol = soup.find('ol')
    #     articles = ol.find_all('article', class_='product_pod')
    #     #print(articles)
    #     for article in articles:
    #         image = article.find('img')
    #         title = image.attrs['alt']
    #         starTag = article.find('p')
    #         star = starTag['class'][1]
    #         price = article.find('p', class_='price_color').text
    #         price = float(price[1:])
    #         # apppending the above items into books Array
    #         books.append([title, star, price])

# parse_url=get_book_info_from_url(liens)

# print(scrap_from_url(parse_url))
