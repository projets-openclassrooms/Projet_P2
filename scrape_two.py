# import des librairies

# variables pour lister urls, liste des categories
categories = []
# fonction parser categories
def label_categories(link):
    # parser des categories
    categories = [a.get_text('href').replace('\n', '') for a in categ.find_all('a')]
    categories = categ.select("ul.breadcrumb>li>a")[-1].text
    return categories
def url_categories(nom):
    # creer liste des liens des categories
    categories_html = [a.get('href') for a in categ.find_all('a')]
    return categories_html


# process pour tester foncctions
