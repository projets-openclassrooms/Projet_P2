import requests
from bs4 import BeautifulSoup as bs

home_url = "https://books.toscrape.com/catalogue/category/books1/"


def extract_transform():
    i= 1

    url_pages = f'{home_url}page-{i}.html'
    for url_book in url_pages:
        for i in range(51):
            page = f'page-{i}.html'
            page_scrapped = f'{home_url}{page}'
            for books in page_scrapped:
                response = requests.get(books)

                # page = reponse.content  # créé une variable avec le contenu de cette réponse
                soup = bs(response.content, "html.parser")
                link = soup.css.select('title')
                print(link)

        pass
    return

extract_transform()