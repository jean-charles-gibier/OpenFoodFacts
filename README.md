# OpenFoodFacts

status : [![CircleCI](https://circleci.com/gh/jean-charles-gibier/OpenFoodFacts.svg?style=shield)](https://app.circleci.com/pipelines/github/jean-charles-gibier/OpenFoodFacts)

## Projet #5 DA Python / OC
 Que souhaitez-vous que votre programme fasse ?

(Bonne question).

Il doit (sur demande) :
- requeter une API REST => faire un PC de quelques lignes capable de ramener une réponse de OFF
- interperéter la réponse en JSON, déterminer sa nature OK 200 / KO x00
- naviquer dans la structure pour en extraire les données utiles
- instancier des objets avec ces données (Categorie, Produit etc.)
- enregistrer ces objets dans une Bdd (en mode raw => par paquet de X000)
- enregistrer les relations entre ce objets
- restituer ces données en fonction de crotères particuliers
- presenter un interface de requetage & administration de la base 

Sur la plan technique / architecture du prg il doit :
- définir un model clair (produit categorie : many 2 many  => + magasins ?) 
- respecter la PEP8 /257
- avoir des packages définis (cf prj 3 / pas de classe fourre tout)
- découpler Presentation  / Model / View 
- etre "object "=> limiter le procedural et les "boucles" / listes de compréhension / principe SOLID etc.
- présenter catégorie / produit avec sous classes => une mission par classe : filtrage / nettoyage / enregistrement 
