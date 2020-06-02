# OpenFoodFacts

status : [![CircleCI](https://circleci.com/gh/jean-charles-gibier/OpenFoodFacts.svg?style=shield)](https://app.circleci.com/pipelines/github/jean-charles-gibier/OpenFoodFacts)

## Projet #5 DA Python / OC
 Que souhaitez-vous que votre programme fasse ?


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
Les fonctionalités requises pour cet exercice sont [décrites ici](https://openclassrooms.com/fr/projects/156/assignment)

Pour exploiter l'interface graphique pygame, le programme va lire un fichier texte (argument '--datafile') 
de 15x15 caractères séparés par des "retour chariot". Chaque ligne de ce fichier représente une ligne du jeu .<br>
Dans cette ligne, chaque caractère symbolise un des éléments suivants (au choix) :
- une case de jeu standard (char ' ' espace ou Ascii 0x20)
- un élément de mur (char '#' hastag)
- la case de départ (char 'S' )
- la case d'arrivée' (char 'E' )

Ce fichier texte est situé dans le repertoire 'resources'.
Le programme interprète le plan du fichier et place 3 items (Aiguille, Tube, Ether) plus un personnage (Gardien), au hasard sur les cases accessibles du plan.<br>
(les items seront disposés de manière à ne pas bloquer le jeu : le garde ne devra pas bloquer l'accès aux items à collecter)

(Bonne question).

Il doit :
- requeter (sur demande) une API REST (faire un POC de quelques lignes capable de ramener une réponse de OFF)
- interperéter la réponse en JSON, déterminer sa nature OK 200 / KO x00
- naviguer dans la structure pour en extraire les données utiles
- instancier des objets avec ces données (Categorie, Produit etc.)
- enregistrer ces objets dans une Bdd (en mode raw => par paquet de X000)
- enregistrer les relations entre ces objets
- restituer ces données en fonction de critères choisis
- presenter une interface de requetage & administration de la base 
- cf user story décrite dans la [présentation du prj](https://openclassrooms.com/fr/projects/157/assignment) 

Sur la plan technique / architecture du prg 
=> il doit :
- définir un model clair (produit categorie : many 2 many  => + magasins ?) 
- respecter la PEP8 /257
- avoir des packages définis (cf prj 3 / pas de classe fourre tout)
- découpler Presentation  / Model / View 
- etre "object "=> limiter le procedural et les "boucles" / listes de compréhension / principe SOLID etc.
- présenter catégorie / produit avec sous classes => une mission par classe : filtrage / nettoyage / enregistrement 

Suivi de l'organisation sur :
[ Jira ](https://jcgibierscompany.atlassian.net/jira/software/projects/CO/boards/2)
