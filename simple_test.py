#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# ajouter l'appel via urllib


with open('D:/github/OCR/garbage/categories2.json', encoding="utf8") as json_file:
    data = json.load(json_file)
    nb_cat = 0
    for p in data['tags']:
        if ((p['id']).startswith('fr:')  ):
            print('Name: ' + p['name'])
            print('Website: ' + p['url'])
            print('Id: ' + p['id'])
            print('')
            nb_cat = nb_cat + 1
    print('Nb categorie :' + str(nb_cat))

# curl --location --request GET 'https://world.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=Saucissons%20secs&json=true'
# avec ça on peut faire une table produit + catégorie