# projet_P2

But du projet :

La version béta de ce script permet de récupérer les informations des produits du site http://books.toscrape.com/.
Il fonctionne en installant python (version utilisée 3.11) et en exécutant quelques commandes.
Ces informations sont les suivantes:

	URL du livre
	Universal Product Code (upc)
	Titre du livre
	Prix, taxe incluse
	Prix, taxe exclue
	Quantité disponible
	Description du produit
	Catégorie
	Notation
	URL de l'image


Elles sont classées par catégories dans un fichier CSV correspondant à la catégorie récupéree.
L'image du livre est aussi récupérée et stockée localement.
Les données sont générées à la racine du projet suivant cette arborescence:

|-- sitescrapped/
    |-- categorie_1/
        |-- categorie_1.csv
        |-- images/
            |-- img1.jpg
            |-- img2.jpg
            ...etc
    |-- categorie_2/
        |-- categorie_2.csv
        |-- images/
            |-- img1.jpg
            |-- img2.jpg
            ...etc


## Installations des requis sous windows
Installation de la dernière version de Python https://www.python.org/download/
Choisissez la manière la plus appropriée d'exécuter vos scripts Python (cmd windows, script bash ou, un IDE tel que pycharm ou VS Code).

Placez vous dans le dossier de votre choix.
git clone https://github.com/bk7191/OpenclassroomsProject-P2.git

## Création de l'environnement virtuel en vue d'installer les librairies
Placez vous dans le dossier cloné, puis créez un nouvel environnement virtuel:
python3 -m venv env
Activez votre environnement virtuel env nouvellement créé 
Sous Windows :
env\scripts\activate.bat

sous linux :
source env/bin/activate

## Installation librairies 
pip install -r requirements.txt

## Utilisation de l'application
Vous pouvez enfin lancer le script:
python scrape_books.py présent à la source du dossier de travail.

## Résultat
Enjoy it.
