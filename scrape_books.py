# -*- coding: utf-8 -*-
from save_scrape import *
from scrape_infos import *

"""
Ce version alpha sert à récupérer :
    - soit toutes les infos concernant un livre,
    - soit les infos concernant tous les livres du site books.toscrape.com

    urls = []  # initialisation de la liste servant à stocker nos urls
    categories = []  # initialisation de la liste des datas
    main_url = "https://books.toscrape.com/"
    h3_tags = soup.find_all("h3")
    récupère les balises h3 contenant les urls des livres
    retire les ../../ en début d'url
    retourne une liste complete d'url
    get_all_url_from_liens(url_liens)
# sert à récupérer chacune des catégories du site
# retourne liste de catégories
   
    get_all_liens(url)
# sert à récupérer les urls de chacune des catégories du site
# réitère même opération que pour les catégories
# retourne url de la catégorie

  # utilisation d'une regex pour isoler le nom de la catégorie dans l'url

"""
home_url = "https://books.toscrape.com/"


# gestion des erreurs de connection sommaire à revoir car bug


def get_all_pages(liens):
    url_liens = liens
    urls = []
    categories = []
    url_liens_temp = url_liens.split("index")[0]
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


def main():
    total_scraped = 1000  # 1000 à recuperer 20 pages * 50 livres
    compteur = 0  # init compteur
    print(f"démarrage du scan du site {home_url}")

    url_category = get_cat_liens(home_url)
    # print(len(url_category), "catégorires scrapées")

    question = input("Voulez-vous tester une catégorie ? O/N ")
    if str.lower(question) == "o":
        i = 0
        for url in url_category:
            print(i, "+" * 2, url['name'], "=" * 2, url['url_cat'])
            i += 1

        choix = input("Merci d'indiquer une catégorie de 0 à 49: ")
        choix_url = url_category[int(choix)]
        print(choix_url['name'], "=" * 2, choix_url['url_cat'], " choisi")

        # match = re.search(r"\/([^\/]+)_\d+\/", choix_url)
        # name = match.group(1)

        scraped_data = scrap_from_url(choix_url, name)
        write_to_csv(scraped_data, name)


    else:
        print("scrape de toutes les catégories du site")
        # print("liens des catégories sauf le home : " ,url_category)
        for url in url_category:
            print("url", url)
            match = re.search(r"\/([^\/]+)_\d+\/", url)
            name = match.group(1)
            print(name, ":")
            url_liens = get_all_pages(url)
            for url_book in url_liens:
                print('book', url_book)
                scraped_data = scrap_from_url(url_liens, name)
                write_to_csv(scraped_data, name)

            compteur += 1  # incrémente le compteur
            total_scraped -= len(url_liens)  # incrémente le total de livres scrapés
            print(
                f"catégorie {compteur} sur {len(url_category)}; dossier : {name} transféré : {len(url_liens)} livres."
            )
            print(f" {total_scraped} livres restants")


if __name__ == "__main__":
    try:
        # dir_clean()  # efface et cree les repertoires de stockage
        main()


    except KeyboardInterrupt:
        print("Programme arrêté manuellement.")
