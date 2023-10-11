import csv
import os
from pathlib import Path

# ecrit les données dans un fichier csv à partir des données et du nom désiré du fichier
current_dir = os.path.dirname(__file__)
folder = os.path.join(current_dir, "/", "site_scraped")



def dir_clean():
    if Path(os.path.exists(folder)):
        Path(folder).parent.rmdir()
    else:
        Path(folder).parent.mkdir(exist_ok=True, parents=True)


def write_to_csv(datas):
    choix_url = {}
    # création des headers

    headers = [
        "product_page_url",
        "universal_product_code",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url",
    ]

    file_path = os.path.join(folder, choix_url.name, f"{name}.csv")
    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(headers)
        writer = csv.DictWriter(file,book_datas)
        n = 0  # initialise un compteur

        for data in datas:
            writer.writerow(data)
            n += 1  # incrémente le compteur
            print('n', n)


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
