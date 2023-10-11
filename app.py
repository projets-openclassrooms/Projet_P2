import os
import shutil
import re
import requests
from bs4 import BeautifulSoup as bts

home_url = "https://books.toscrape.com/"
index_url = f"{home_url}index.html"
cat_url = f"{home_url}catalogue"


# Création des répertoires


def creation_folder():
    try:
        os.mkdir('livres/')
        os.mkdir('couvertures/')
    except OSError:
        pass


def sans_ponctuation(ponctuation):
    # .replace(',', '').replace(';', '')
    sans = re.sub(r'[,;.]', "", ponctuation)
    return sans


def sans_monnaie(monnaie):
    rien = re.sub(r'[ Â£]', "", monnaie)
    return rien


def remove_bad_char(test_string):
    # initializing bad_chars_list
    # bad_chars = [';', ':', '!', "*", " ", "#", "â", '.', '/', '~','&','\',','{',"}"]

    new_string = re.sub(r'[<>;.:,"/\|?*&€%£$()~#{}=+°-]', "_", test_string)
    new_string = re.sub(r'[@â]', "a", new_string)
    new_string = re.sub(r'&', "et", new_string)
    new_string = re.sub(r'ù', "u", new_string)

    return new_string


def delete_folder():
    repertoire_de_travail = str(os.path.dirname(os.path.realpath(__file__)))
    # print (repertoire_de_travail)
    dossier_livres = os.path.join((repertoire_de_travail + '/livres/'))
    dossier_couvertures = os.path.join((repertoire_de_travail + '/couvertures/'))
    # print(dossier_livres)
    if os.path.exists(dossier_livres):
        shutil.rmtree(dossier_livres, ignore_errors=False, onerror=None)
        shutil.rmtree(dossier_couvertures, ignore_errors=False, onerror=None)


# Traitement de la page pour chercher nombre pages des categories


def get_page_categorie(link_cat, cat):
    link_cat = link_cat.replace('index.html', 'page-1.html')
    response_cat_page = requests.get(link_cat)
    if response_cat_page.ok:
        i = 1
        while response_cat_page.ok:
            #
            get_books_on_page(link_cat, cat)
            i = i + 1
            link_cat = link_cat.replace('page-' + str(i - 1) + '.html', 'page-' + str(i) + '.html')
            # print(link_cat)
            response_cat_page = requests.get(link_cat)
    else:
        link_cat = link_cat.replace('page-1.html', 'index.html')
        get_books_on_page(link_cat, cat)


# Récupération des livres d'une catégorie


def get_books_on_page(link, cat):
    response_page = requests.get(link)
    books_links = bts(response_page.text, features="html.parser")
    liens_livres = books_links.findAll('div', {'class': 'image_container'})
    # print(liens_livres)
    for i in range(len(liens_livres)):
        save_books(liens_livres[i].find('a').attrs['href'].replace('../../..', cat_url), cat)
    # print(liens_livres)


# Récupération des infos d'un livre


def save_books(link, cat):
    response_book_page = requests.get(link)
    if response_book_page.ok:
        with open('livres/' + cat + '.csv', 'a', encoding='utf-8-sig') as file:
            soup = bts(response_book_page.text, features="html.parser")
            tds = soup.findAll('td')
            u_p_c = tds[0].text
            u_p_c = sans_ponctuation(u_p_c)
            p_i_t = tds[3].text.replace('£', "").replace('Â', "")
            p_i_t = sans_ponctuation(p_i_t)
            p_e_t = tds[2].text.replace('£', "").replace('Â', "")
            p_e_t = sans_ponctuation(p_e_t)
            num_avble = tds[5].text.replace('In stock (', '').replace(' available)', "")
            review_rating = tds[6].text
            review_rating = sans_ponctuation(review_rating)

            title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text
            title = sans_ponctuation(title)

            prod_desc = soup.find('article', {'class': 'product_page'}).findAll('p')[3].text
            prod_desc = sans_ponctuation(prod_desc)

            category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text
            category = sans_ponctuation(category)
            image_url = soup.find('div', {'class': 'item active'}).find('img').attrs['src'].replace('../..', home_url)
            dwld_imgs(image_url, title, u_p_c)
            resultat = link + ';' + u_p_c + ';' + title + ';' + p_i_t + ';' + p_e_t + ';' + num_avble + ';' + prod_desc + ';' + category + ';' + review_rating + ';' + image_url + '\n'
            file.write(resultat)


# Téléchargement des couvertures


def dwld_imgs(image_url, title, product_code):
    response = requests.get(image_url)
    file = open('couvertures/' + remove_bad_char(title) + product_code + '.jpg', "wb")
    file.write(response.content)
    file.close()


def main():
    delete_folder()
    creation_folder()
    response = requests.get(index_url)
    headers = 'product_page_url;universal_product_code;title;price_including_tax;price_excluding_tax;number_available' \
              ';product_description;category;review_rating;image_url\n'
    if response.ok:
        cat_links = bts(response.text, features="html.parser")
        cat_link = cat_links.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('a')
        # print(cat_Link)
        for i in range(len(cat_link)):
            # print(cat_Link[i])
            with open('livres/' + cat_link[i].text.replace('\n', '').replace(' ', '') + '.csv', 'w',
                      encoding='utf-8-sig') as file:
                file.write(headers)
            print('Catégorie : ' + cat_link[i].text.replace('\n', '').replace(' ',
                                                                              '') + ' ' + str(
                i + 1) + '/' + str(len(cat_link)))
            # fonction pour rechercher les liens des categories
            get_page_categorie(home_url + cat_link[i].attrs['href'],
                               cat_link[i].text.replace('\n', '').replace(' ', ''))
            print("téléchargement terminé")


if __name__ == "__main__":
    try:

        main()

    except KeyboardInterrupt:
        print("Programme arrêté manuellement.")
