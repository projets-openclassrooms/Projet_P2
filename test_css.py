import requests
from bs4 import BeautifulSoup as bs

home_url = "https://books.toscrape.com/catalogue/category/books1/"


def extract_transform():
    i = 1
    pages = {}

    url_pages = f'{home_url}page-{i}.html'
    for url_book in url_pages:
        for i in range(51):
            page = f'page-{i}.html'
            page_scrapped = f'{home_url}{page}'
            pages = {'page': page_scrapped}
        # print(pages)

    for page in pages.keys():
        id = page
        lien = pages[page]
        print(id, lien)
        response = requests.get(lien)
        #     #
       # page = reponse.content  # créé une variable avec le contenu de cette réponse
        soup = bs(response.content, "html.parser")
        link = soup.css.select('title')
        print(link)

    pass


    return link

extract_transform()
