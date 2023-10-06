import csv
import os
from pathlib import Path
import slugify
# ecrit les données dans un fichier csv à partir des données et du nom désiré du fichier
current_dir = os.path.dirname(__file__)
folder = os.path.join(current_dir, "/", "site_scraped")


def clean_name(name):
    cleaned_name = re.sub(r'[<>;:"/\\|?*]', "-", name)
    return cleaned_name


def dir_clean():
    if Path(os.path.exists(folder)):
        Path(folder).parent.rmdir()
    else:
        Path(folder).parent.mkdir(exist_ok=True, parents=True)


def write_to_csv(datas, name):
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

    file_path = os.path.join(folder, name, f"{name}.csv")
    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(headers)
        n = 0  # initialise un compteur

        for data in datas:
            writer.writerow(data)
            n += 1  # incrémente le compteur
            print('n', n)
