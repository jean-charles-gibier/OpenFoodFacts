#!/usr/bin/python3
# coding: utf-8

import requests
#import pprint
from core import utils
import logging as lg

logger = lg.getLogger(__name__)

# TODO : comment in english
# limite nb de produits par catégorie
# (en dessous de laquelle on ne charge pas les produits attachés)
LOW_LIMIT_NB_PRODUCTS = 10000
# default nb de catégories max à charger (overlaps LOW_LIMIT_NB_PRODUCTS)
LIMIT_NB_CATEGORIES = 20
# default country origin
DEFAULT_COUNTRY_ORIGIN = "France"
# service API url for categories
API_URL_CATEGORIES="https://fr.openfoodfacts.org/products/categories"
# service API url for categories
API_URL_PRODUCTS="https://fr.openfoodfacts.org/cgi/search.pl"
# default nb de produits  max à charger (chunk size)
LIMIT_NB_PRODUCTS = 1000



class CategoryDownloader:
    """ Download categories from OFF API
    origin : pays d'origine des relevés
    number : nombre de relevés
    lower_limit : nombre de produits minimum pour selectionner la categorie
    """

    def fetch(self, origin=DEFAULT_COUNTRY_ORIGIN, number=LIMIT_NB_CATEGORIES, lower_limit=LOW_LIMIT_NB_PRODUCTS):
        """ Fetch products from OFF API """
        payload = {
            "origins": origin,
            "page_size": number,
            "json": 1,
        }

        response = requests.get(
            API_URL_CATEGORIES, params=payload)
        data = response.json()
        # on ne selectionne que les catégories avec un nombre "consequent" de produits
        return [categorie["name"] for categorie in data['tags'] if categorie["products"] > lower_limit]




class ProductDownloader:
    """ Download products from OFF API """
    _page_counter = 0

    def reset_page_counter(self):
        """ reset page counter """
        self._page_counter = 0

    @property
    def page_counter(self):
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
            "fields": 'code,categories,url,stores,nutrition_grade_fr',
            "json": 1
        }

        response = requests.get(
            API_URL_PRODUCTS, params=payload)
        data = response.json()
        products = data['products']
        self._page_counter = self._page_counter + 1
        if len(products) > 0:
            return products


def main():
    # prepare les logs
    utils.set_logger()
    category_downloader = CategoryDownloader()
    category_list = category_downloader.fetch('France', LIMIT_NB_CATEGORIES)


    product_downloader = ProductDownloader()
    for each_category in category_list:

        # record the current category
        # get id
        # for each products => raw write products
        #                   => raw write join table product / category
        #   put indexes.

        product_downloader.reset_page_counter()

        while True:
        # parametrizer
            products = product_downloader.fetch(each_category, LIMIT_NB_PRODUCTS)
            if products == None:
                break
            for product in products:
                try:
                    pass
    #                pprint.pprint(sorted(product.items()))
    #                product = Product.objects.create_from_openfoodfacts(**product)
                except TypeError:
                    continue

            logger.debug('Get page #%d  ', product_downloader.page_counter)

if __name__ == "__main__":
    main()
