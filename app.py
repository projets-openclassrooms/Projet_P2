import os
import shutil

import requests
from bs4 import BeautifulSoup as bts

home_url = "https://books.toscrape.com/"
index_url = f"{home_url}index.html"
cat_url = f"{home_url}catalogue"


def main():
    delete_folder()
    creation_folder()
    response = requests.get(index_url)
    headers = 'product_page_url;universal_product_code;title;price_including_tax;price_excluding_tax;number_available;product_description;category;review_rating;image_url\n'
    if response.ok:
        cat_Links = bts(response.text, features="html.parser")
        cat_Link = cat_Links.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('a')
        # print(cat_Link)
        for i in range(len(cat_Link)):
            # print(cat_Link[i])
            with open('livres/' + cat_Link[i].text.replace('\n', '').replace(' ', '') + '.csv', 'w',
                      encoding='utf-8-sig') as file:
                file.write(headers)
            print('Catégorie en cours de téléchargement : ' + cat_Link[i].text.replace('\n', '').replace(' ',
                                                                                                         '') + ' ' + str(
                i + 1) + '/' + str(len(cat_Link)))
            pagecat(home_url + cat_Link[i].attrs['href'], cat_Link[i].text.replace('\n', '').replace(' ', ''))



# Création des répertoires


def creation_folder():
    try:
        os.mkdir('livres/')
        os.mkdir('couvertures/')
    except OSError:
        pass
    else:
        pass


def delete_folder():
    repertoire_de_travail = str(os.path.dirname(os.path.realpath(__file__)))
    #print(repertoire_de_travail)
    dossier_livres = os.path.join((repertoire_de_travail+'/livres/'))
    dossier_couvertures  = os.path.join((repertoire_de_travail+'/couvertures/'))
    #print(dossier_livres)
    if os.path.exists(dossier_livres):
        shutil.rmtree(dossier_livres, ignore_errors=False, onerror=None)
        shutil.rmtree(dossier_couvertures, ignore_errors=False, onerror=None)
    else:
        pass


# Traitement de la pagination


def pagecat(linkCat, cat):
    linkCat = linkCat.replace('index.html', 'page-1.html')
    responseCatPage = requests.get(linkCat)
    if responseCatPage.ok:
        i = 1
        while responseCatPage.ok:
            onepage(linkCat, cat)
            i = i + 1
            linkCat = linkCat.replace('page-' + str(i - 1) + '.html', 'page-' + str(i) + '.html')
            responseCatPage = requests.get(linkCat)
    else:
        linkCat = linkCat.replace('page-1.html', 'index.html')
        onepage(linkCat, cat)


# Récupération des livres d'une catégorie


def onepage(link, cat):
    responsePage = requests.get(link)
    booksLinks = bts(responsePage.text, features="html.parser")
    liens_livres = booksLinks.findAll('div', {'class': 'image_container'})
    for i in range(len(liens_livres)):
        savebooks(liens_livres[i].find('a').attrs['href'].replace('../../..', cat_url), cat)
    #print(liens_livres)


# Récupération des infos d'un livre


def savebooks(link, cat):
    responseBookPage = requests.get(link)
    if responseBookPage.ok:
        with open('livres/' + cat + '.csv', 'a', encoding='utf-8-sig') as file:
            soup = bts(responseBookPage.text, features="html.parser")
            tds = soup.findAll('td')
            u_p_c = tds[0].text.replace(',', '').replace(';', '')
            p_i_t = tds[3].text.replace(',', '').replace(';', '').replace('£', "").replace('Â',"")
            p_e_t = tds[2].text.replace(',', '').replace(';', '').replace('£', "").replace('Â',"")
            num_avble = tds[5].text.replace('In stock (','').replace(' available)',"")
            reviewRating = tds[6].text.replace(',', '').replace(';', '')
            title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text.replace(',', '').replace(';',
                                                                                                                  '')
            prod_desc = soup.find('article', {'class': 'product_page'}).findAll('p')[3].text.replace(',',
                                                                                                     '').replace(
                ';', '')
            category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text.replace(',', '').replace(';', '')
            imageUrl = soup.find('div', {'class': 'item active'}).find('img').attrs['src'].replace('../..', home_url)
            dwld_imgs(imageUrl, u_p_c)
            resultat = link + ';' + u_p_c + ';' + title + ';' + p_i_t + ';' + p_e_t + ';' + num_avble + ';' + prod_desc + ';' + category + ';' + reviewRating + ';' + imageUrl + '\n'
            file.write(resultat)


# Téléchargement des couvertures


def dwld_imgs(imageUrl, productCode):
    response = requests.get(imageUrl)
    file = open('couvertures/' + productCode + '.jpg', "wb")
    file.write(response.content)
    file.close()


def main():
    delete_folder()
    creation_folder()
    response = requests.get(index_url)
    headers = 'product_page_url;universal_product_code;title;price_including_tax;price_excluding_tax;number_available;product_description;category;review_rating;image_url\n'
    if response.ok:
        cat_Links = bts(response.text, features="html.parser")
        cat_Link = cat_Links.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('a')
        # print(cat_Link)
        for i in range(len(cat_Link)):
            # print(cat_Link[i])
            with open('livres/' + cat_Link[i].text.replace('\n', '').replace(' ', '') + '.csv', 'w',
                      encoding='utf-8-sig') as file:
                file.write(headers)
            print('Catégorie : ' + cat_Link[i].text.replace('\n', '').replace(' ',
                                                                              '') + ' ' + str(
                i + 1) + '/' + str(len(cat_Link)))
            pagecat(home_url + cat_Link[i].attrs['href'], cat_Link[i].text.replace('\n', '').replace(' ', ''))


if __name__ == "__main__":
    try:

        main()

    except KeyboardInterrupt:
        print("Programme arrêté manuellement.")
