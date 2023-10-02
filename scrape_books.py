# -*- coding: utf-8 -*-
import os
import re

import requests
from bs4 import BeautifulSoup as bs
from scrape_infos import scrap_from_url
from save_scrape import write_to_csv

""" source inspiration site pythondoctor
sert à récupérer toutes les url d'une seule catégorie
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
clear = lambda: os.system("cls")


# gestion des erreurs de connection sommaire à revoir car bug
def test_connection(url):
    try:
        reponse = requests.get(url_liens)
    except requests.exceptions.RequestException as erreur:  # affiche l'erreur renvoyée
        print(erreur)


def get_all_url_from_liens(url_liens):
    urls = []
    categories = []
    url_liens_temp = url_liens.split("index")[0]
    while True:
        try:
            reponse = requests.get(url_liens)
        except (
            requests.exceptions.RequestException
        ) as erreur:  # affiche l'erreur renvoyée
            print(erreur)
        page = reponse.content
        soup = bs(page, "html.parser")

        urls.append(url_liens)

        try:
            next_page = soup.find("li", class_="next").find("a")
        except:
            break

        if next_page is not None:
            url_liens = next_page["href"]
            url_liens = url_liens_temp + url_liens

    for url in urls:
        try:
            reponse = requests.get(url)
        except requests.exceptions.RequestException as e:  # affiche l'erreur renvoyée
            print(e)
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


def get_all_liens(url):
    try:
        reponse = requests.get(url)
    except requests.exceptions.RequestException as erreur:
        print(erreur)
    page = reponse.content  # créé une variable avec le contenu de cette réponse
    soup = bs(
        page, "html.parser"
    )  # parse la variable via le parser de BeautifulSoup (gagner en lisibilité)
    data = []  # initialisation de la liste qui stocke les urls
    all_cat = soup.find(
        "ul", class_="nav nav-list"
    )  # isole la classe nav nav-list de la balise ul
    hrefs = all_cat.find_all("a", href=True)
    for href in hrefs:  # parcourt les valeurs des hrefs extraits au dessus
        href = href["href"]  # extrait la valeur seule de href
        url = f"{home_url}{href}"
        data.append(url)  # ajoute l'url à la liste de données à retourner
    data.pop(0)

    return data


"""
# to run the script. 
"""


def main():
    total_scraped = 0
    n = 0  # compteur
    print(f"démarrage du scan du site {home_url}")

    url_home = f"{home_url}index.html"  # url de l'accueil du site
    url_category = get_all_liens(url_home)
    question = input("Voulez-vous tester une catégorie ? O/N ")
    if str.lower(question) == "o":
        i=0
        for url in url_category:
            print(i, "+"*2, url)
            i+=1
            choix = input("Merci d'indiquer une catégorie de 0 à 49 :")
            url_categorie = url_category[int(choix)]
        match = re.search(r"\/([^\/]+)_\d+\/", url_categorie)
        name = match.group(1)
        url_liens = get_all_url_from_liens(url_categorie)
        scraped_data = scrap_from_url(url_liens, name)
        write_to_csv(scraped_data, name)
        n += 1  # incrémente le compteur
        total_scraped += len(
            url_liens
        )  # incrémente le total de livres scrapés de la catégorie
        print(
            f"catégorie {n} sur {len(url_category)}; dossier : {name} transféré en local avec {len(url_liens)} livres scrapé(s)"
        )
        clear()
    else:
        print("scrape de toutes les catégories du site")
        #print("liens des catégories  sauf le home : ",url_category)
        for url in url_category:
            match = re.search(r"\/([^\/]+)_\d+\/", url)
            name = match.group(1)
            print(name, ":")
            url_liens = get_all_url_from_liens(url)
            scraped_data = scrap_from_url(url_liens, name)
            write_to_csv(scraped_data, name)
            n += 1  # incrémente le compteur
            total_scraped += len(url_liens)  # incrémente le total de livres scrapés
            print(
                f"catégorie {n} sur {len(url_category)}; dossier : {name} transféré en local avec {len(url_liens)} livres scrapé(s)"
            )
    print(f" {total_scraped} livres scrapés")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programme arrêté manuellement.")
