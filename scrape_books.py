# -*- coding: utf-8 -*-
import os

from scrape_infos import *

"""
Ce version béta sert à récupérer :
    - soit toutes les infos concernant un livre,
    - soit les infos concernant tous les livres du site books.toscrape.com
selon la méthode Extract Transform Load
Extract :
    scrape_books.py
    home_url = "https://books.toscrape.com/"
    url_category = get_cat_liens(home_url) pour lister les categories
 
Transform :
    scrape_infos.py
    scrap_category(liens) pour recuperer les livres par categorie
    
    :return noms, liens, UPC, noms des images, catégories, etc...

Load:
    save_scrape.py
    write_to_csv(upc)   
infos connues
#home_url = books.toscrape.com

infos inconnues
#url book = home_url + id = write_review ('catalogue/ + a-light-in-the-attic_1000 + /index.html par exemple)
# url image = home_url + img src de div class =" item active"
#url categorie = home_url + catalogue/category/books + {nom categorie} + page + nbre livres par categorie

"""
home_url = "https://books.toscrape.com/"

"""
recherche categories 
with csvfile:
    question 
        categorie
            lister categories
             afficher liste categories
                a = stocker liste categories
                question choix categorie
                    categorie choisie
                    remplacer lien index.html par page-1.html
                    chercher form horizontal nombres livres
                    compter nbpages = ceil(n/20)
                    for i in nbpages:
                        creer lien page-i.html
                        scrape page _i.html
                        def lien_livre = chercher href lien livres => stocker_livres
                        remplacer caracteres ../ par home_url+ lien
                        ajout dans csvfile
                        close csvfile
        toutes categories
            with liste categories
                remplacer lien index.html par page-1.html
                chercher form horizontal nombres livres
                compter nbpages = ceil(n/20)
                for i in nbpages:
                    creer lien page-i.html
                    scrape page _i.html
                    def lien_livre = chercher href lien livres => stocker_livres
                    remplacer caracteres ../ par home_url+ lien
                    ajout dans csvfile
                    close csvfile
                        
                                        compter 
        toutes categories    




"""
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
        print(choix_url['name'], "=" * 2, choisi, " choisi.")
        liens = f"{home_url}{choisi}"
        #1 choix x livres
        scraped_data = scrap_category(liens)

        parse_url = contenu_livres(get_book_info_from_url(scraped_data))
        #scraped_data = scrap_category(liens)
        # for url_book in parse_url:
        print('book', "++", parse_url['title'])
        # scraped_data = get_book_info_from_url(parse_url['product_page_url'])
        # print(scraped_data)
        # write_to_csv(scraped_data)

        # scraped_data = books_url(choix_url, name)

        # script pour charger les données dans un csv
        # write_to_csv(scraped_data, name)

    else:
        print("scrape de toutes les catégories du site")
        print("liens des catégories sauf le home : " ,url_category)
        for liens_book in url_category:
            liens = (f"{home_url}" + liens_book['url_cat'])
            # match = re.search(r"\/([^\/]+)_\d+\/", url)
            # name = match.group(1)
            print(liens, ":")
            parse_url = contenu_livres(liens)
            # url_liens = get_all_pages(liens)
            # recursivite des donnees à recuperer
            for url_book in liens_book:
                print('book', url_book)
                # scraped_data = get_book_info_from_url(url_book)
                # write_to_csv(scraped_data)

            # compteur += 1  # incrémente le compteur
            # total_scraped -= len(url)  # incrémente le total de livres scrapés
            # print(
            #     f"catégorie {compteur} sur {len(url_category)}; dossier : {name} transféré : {len(url_liens)} livres."
            # )
            # print(f" {total_scraped} livres restants")


if __name__ == "__main__":
    try:
        # dir_clean()  # efface et cree les repertoires de stockage
        #main()
        pass

    except KeyboardInterrupt:
        print("Programme arrêté manuellement.")


def execute_prog():

    # ecrit les données dans un fichier csv à partir des données et du nom désiré du fichier
    current_dir = os.path.dirname(__file__)
    print(current_dir)
    #efface dossier depart
    #def dir_clean()

    total_scraped = 1000  # 1000 à recuperer 20 pages * 50 livres
    compteur = 0  # init compteur
    print(f"démarrage du scan du site {home_url}")
    # recuperer la liste des categories
    url_category = get_cat_liens(home_url)
    # 1 ou toutes les categories?
    # execute la creation des dossiers et doc csv de stockage
    question = input("Voulez-vous tester une catégorie ? O/N ")
    if str.lower(question) == "o":
        #numerote categories de 0 à 49
        i = 0

        for url in url_category:
            print(i, "+" * 2, url['name'], "=" * 2, url['url_cat'])
            i += 1
        choix = input("Merci d'indiquer une catégorie de 0 à 49: ")
        choix_url = url_category[int(choix)]
        choisi = choix_url['url_cat']
        #afficher le numero de categorie choisi pour scraper
        print(choix_url['name'], "=" * 2, choisi, " choisi.")
        liens = f"{home_url}{choisi}"


        #scrape la categorie pour en extraire son nombre de livres
        #parse_url = contenu_livres(get_book_info_from_url(liens))

        scraped_data = scrap_category(liens) #??
        parse_url = contenu_livres(get_book_info_from_url(liens))

        # affiche le titre du livre scrape
        #print('book', "++", parse_url['title'])
        # affiche le nombre restant à scraper
        #total_scraped -= scraped_data
        # ferme le fichier csv

    else:
        # choix scrape toutes categories
        print("scrape de toutes les catégories du site")
        for liens_book in url_category:
            liens = (f"{home_url}" + liens_book['url_cat'])
            parse_url = contenu_livres(liens)
            for url_book in liens_book:
                print('book', url_book)
execute_prog()