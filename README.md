# projet_P2

But du projet : Utilisez les bases de Python pour l'analyse de marché en récupérant la totalité d'un site 'https://books.toscrape.com/'
contenant les informations de livres et les stocker dans un fichier local au format csv.

## Installations des requis sous windows
Installation python 3.11 sur la machine
Clone du repository sur la machine pour récupérer le code :
git clone https://github.com/bk7191/OpenclassroomsProject-P2.git

## Création de l'environnement virtuel en vue d'installer les librairies
python3 -m venv env
Activez votre environnement virtuel env nouvellement créé.
source env/bin/activate

## Installation librairies 
pip install -r requirements.txt

## Utilisation de l'application
Lancer simplement le script python scrape_one.py présent à la source du dossier de travail.

## Résultat
Une fois le script exécuté, le résultat se trouvera dans le dossier datas/ pour les données et img/ pour les couvertures des livres.

Dans le fichier csv du répertoire datas, il y aura les informations demandées.
