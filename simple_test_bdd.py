#!/usr/bin/python3
# coding: utf-8

import requests
import pprint


class CategoryDownloader:
    """ Download categories from OFF API
    origin : pays d'origine des relevés
    number : nombre de relevés
    lower_limit : nombre de produits minimum pour selectionner la categorie
    """

    def fetch(self, origin="France", number=20, lower_limit=10000):
        """ Fetch products from OFF API """
        payload = {
            "origins": origin,
            "page_size": number,
            "json": 1,
        }

        response = requests.get(
            "https://fr.openfoodfacts.org/products/categories", params=payload)
        data = response.json()
        # on ne selectionne que les catégories avec un nombre "consequent" de produits
        return [categorie["name"] for categorie in data['tags'] if categorie["products"] > lower_limit]




class ProductDownloader:
    """ Download products from OFF API """
    _page_counter = 0

    def reset_page_counter(self):
        """ reset page counter """
        self._page_counter = 0

    def get_page_counter(self):
        """ get page counter """
        return self._page_counter

    def fetch(self, categorie, number=20):
        """ Fetch products from OFF API """
        payload = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": categorie,
            "page_size": number,
            "page" : self._page_counter,
            "fields": 'categories,url,stores,nutrition_grade_fr',
            "json": 1
        }

        response = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl", params=payload)
        data = response.json()
        self._page_counter = self._page_counter + 1
        return data['products']


def main():
    category_downloader = CategoryDownloader()
    category_list = category_downloader.fetch('France', 3)


    product_downloader = ProductDownloader()
    for each_category in category_list:
        products = product_downloader.fetch(each_category, 500)
        for product in products:
            try:
                pprint.pprint(sorted(product.items()))
# product = Product.objects.create_from_openfoodfacts(**product)
            except TypeError:
                continue

if __name__ == "__main__":
    main()
