# OpenFoodFacts

status : [![CircleCI](https://circleci.com/gh/jean-charles-gibier/OpenFoodFacts.svg?style=shield)](https://app.circleci.com/pipelines/github/jean-charles-gibier/OpenFoodFacts)

## Projet #5 DA Python / OC

Les scripts **pur_beurre.py** et **client_pur_beurre.py** forment une suite interagissant avec la base Open Food Facts pour en récupérer les aliments, les comparer et proposer à l'utilisateur un substitut plus sain à l'aliment qui lui fait envie.

(Les besoins du projet sont [décrits ici](https://openclassrooms.com/fr/projects/157/assignment))

Le programme **pur_beurre.py** orésente le fonctionalités suivantes :

- requeter sur demandel'API REST Openfastfood
- interperéter la réponse en JSON, déterminer sa nature (OK 200 / KO x00)
- naviguer dans la structure pour en extraire les données utiles
- instancier des objets avec ces données (Categorie, Produit, substitut etc.)
- enregistrer ces objets dans une base de données (en mode raw => par paquet de X000)
- enregistrer les relations entre ces objets
- restituer ces données en fonction de critères choisis (mots clés ou catégorie)
- presenter une suite de services au programme **client_pur_beurre.py** 

Le programme **client_pur_beurre.py**  est une interface exploitant les fonctionalités de **pur_beurre.py**.
Cette interface présente une suite de menus en mode texte. (Les différentes "user stories" seront définies en fonction de la navigation dans l'arborescence du menu).

Sur la plan technique / architecture, ces deux programmes programmes doivent :
- définir un model clair (produit categorie substitus, many 2 many) 
- respecter la PEP8 /257
- avoir des packages définis (pas de classe "fourre tout")
- découpler Presentation  / Model / View 
- etre "objet "=> limiter le procedural et les "boucles" / listes de compréhension / principe SOLID etc.
- présenter catégorie / produit avec sous classes => une mission par classe : filtrage / nettoyage / enregistrement 

La planification du projet a été organisée sur :
[ Jira ](https://jcgibierscompany.atlassian.net/jira/software/projects/CO/boards/2)


# pur beurre
Cours python Openclassrooms 3eme mission

## installation

Prérequis : 
- Serveur mysql installé<br>
(testé sur : Mysql Community Server 8.0.20)
- Accès internet a l'api du site OpenFoodFacts

installer le projet :
````
# git pull <this repo>
````
installer la base
````
# cd sql
# mysql -<options> < init.sql
````
modifier la configuration
````
# cd ../resources
# vim database.json.to_configure
````
modifier les parametres de connexion et savegarder sous 'database.json'


lancer/tester
````
# pip install -r requirements.txt
# python3 pur_beurre.py -h
# python3 client_pur_beurre.py 
````




## usage
````
usage: macgyver.py [-h] [-d DATAFILE]

optional arguments:
  -h, --help            show this help message and exit# description des fonctionalités

  -d DATAFILE, --datafile DATAFILE.TXT
                        file containing map of labyrinth
  -i {Graphic,Text}, --interface {Graphic,Text}
                        Display interface : 'text' or 'graphic'
````
# description des fonctionalités
