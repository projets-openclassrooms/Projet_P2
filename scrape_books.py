# -*- coding: utf-8 -*-
from save_scrape import *
from scrape_infos import *

"""
Ce version alpha sert à récupérer :
    - soit toutes les infos concernant un livre,
    - soit les infos concernant tous les livres du site books.toscrape.com
selon la méthode Extract Transform Load
Extract :
    urls = []  # initialisation de la liste servant à stocker nos urls
    categories = []  # initialisation de la liste des datas
    home_url = "https://books.toscrape.com/"
    h3_tags = soup.find_all("h3")
    récupère les balises h3 contenant les urls des livres
Transform :
    retire les ../../ en début d'url
    retourne une liste complete d'url
    get_all_url_from_liens(url_liens)
    :return noms, liens, UPC, noms des images, catégories 

 retourne liste de catégories
   
    get_all_liens(url)
# sert à récupérer les urls de chacune des catégories du site
# réitère même opération que pour les catégories
# retourne url de la catégorie

  # utilisation d'une regex pour isoler le nom de la catégorie dans l'url

"""
home_url = "https://books.toscrape.com/"




def main():
    total_scraped = 1000  # 1000 à recuperer 20 pages * 50 livres
    compteur = 0  # init compteur
    print(f"démarrage du scan du site {home_url}")
    # recherche des categories
    url_category = get_cat_liens(home_url)
    # print(len(url_category), "catégorires scrapées") = 50
    # menu pour sélectionner 1 catégorie sur 50 (liste de 0 à 49)

    question = input("Voulez-vous tester une catégorie ? O/N ")
    if str.lower(question) == "o":
        i = 0
        for url in url_category:
            print(i, "+" * 2, url['name'], "=" * 2, url['url_cat'])
            i += 1
        # input pour choisir la catégorie à transformer
        choix = input("Merci d'indiquer une catégorie de 0 à 49: ")
        choix_url = url_category[int(choix)]
        choisi = choix_url['url_cat']
        print(choix_url['name'], "=" * 2, choisi, " choisi")
        liens = (f"{home_url}{choisi}")

        # match = re.search(r"\/([^\/]+)_\d+\/", choix_url)
        # name = match.group(1)
        scraped_data = scrap_category(liens)

        #scraped_data = scrap_from_url(choix_url, name)
        #script pour charger les données dans un csv
        #write_to_csv(scraped_data, name)


    else:
        print("scrape de toutes les catégories du site")
        # print("liens des catégories sauf le home : " ,url_category)
        for url in url_category:
            liens = (f"{home_url}"+url['url_cat'])
            # match = re.search(r"\/([^\/]+)_\d+\/", url)
            # name = match.group(1)
            print(liens, ":")
            #url_liens = get_all_pages(liens)
            # for url_book in url_liens:
            #     print('book', url_book)
            #     scraped_data = scrap_from_url(url_liens, name)
            #     write_to_csv(scraped_data, name)

            # compteur += 1  # incrémente le compteur
            # total_scraped -= len(url)  # incrémente le total de livres scrapés
            # print(
            #     f"catégorie {compteur} sur {len(url_category)}; dossier : {name} transféré : {len(url_liens)} livres."
            # )
            # print(f" {total_scraped} livres restants")


if __name__ == "__main__":
    try:
        # dir_clean()  # efface et cree les repertoires de stockage
        main()


    except KeyboardInterrupt:
        print("Programme arrêté manuellement.")
