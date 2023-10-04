import os
import re
import requests

"""
regex pour nettoyer le nom du fichier <>:"/\\|?* en les remplaçant par "-"
download_img
#télécharger l'image depuis son url sous le nom du livre associé et dans un dossier avec le nom de la catégorie associée
#création des dossiers 'scrapped' et categories s'il n'existent pas déjà
#utilisation de f'strings pour éviter problèmes caractères chainés

"""


def clean_name(name):
    cleaned_name = re.sub(r'[<>;:"/\\|?*]', "-", name)
    return cleaned_name


def download_img(img_url, name, category):
    if not os.path.exists("site_scraped"):
        os.makedirs("site_scraped")

    if not os.path.exists(f"site_scraped\{category}"):
        os.makedirs(f"site_scraped\{category}")

    name = clean_name(name)
    file_path = os.path.join("site_scraped", category, f"{name}.jpg")

    with open(file_path, "wb") as images:
        response = requests.get(img_url)

        if not response.ok:
            print(response)
        else:
            print("Téléchargement de l'image.", name)

        images.write(response.content)


# download_img('https://books.toscrape.com/catalogue/sharp-objects_997/index.html','Sharp Objects','mystery')
