produits = {'a897fe39b1053632': {'title': 'A Light in the Attic',
                                 'product_page_url': 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
                                 'price_incl_tax': '51.77',
                                 'price_excl_tax': '51.77',
                                 'product_description': "bla,bla",
                                 'category': 'Poetry',
                                 'review_rating': '0',
                                 'stock': '22',
                                 'image_url': 'https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg',
                                 }}

for produit in produits.keys():
    UPC = produit
    Titre = produits[produit]['title']
    prix_HT = produits[produit]['price_excl_tax']
    prix_TTC = produits[produit]['price_incl_tax']
    catégorie = produits[produit]['category']
    lien = produits[produit]['product_page_url']
    print(f"{UPC:<16} {Titre:<17} {lien:<17} {prix_HT:>8} {prix_TTC:>8} {catégorie:>28}")

