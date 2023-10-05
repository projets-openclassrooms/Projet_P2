import csv
import os


# ecrit les données dans un fichier csv à partir des données et du nom désiré du fichier

def clean_name(name):
    cleaned_name = re.sub(r'[<>;:"/\\|?*]', "-", name)
    return cleaned_name

def dir_clean():
    try:
        os.rmdir('site_scraped/')
        os.rmdir('livres/')
        os.rmdir('couvertures/')
    except OSError:
        pass
    else:
        os.mkdir('site_scraped/')
        os.mkdir('livres/')
        os.mkdir('couvertures/')



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

    file_path = os.path.join("site_scraped", name, f"{name}.csv")
    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(headers)
        n = 0  # initialise un compteur

        for data in datas:
            writer.writerow(data)
            n += 1  # incrémente le compteur
