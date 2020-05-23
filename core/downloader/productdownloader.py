import requests

from core import constant


class ProductDownloader:

    """ defines product object"""
    # collectionof caotegorie
    _list_products = []

    """ Download products from OFF API """
    _page_counter = 1

    def reset_page_counter(self):
        """ reset page counter """
        self._page_counter = 1

    @property
    def list_products(self):
        """ get page counter """
        return self._list_products

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
            "page": self._page_counter,
            "fields": 'code,brands,url,stores,nutrition_grade_fr,product_name,generic_name_fr',
            "json": 1
        }

        response = requests.get(
            constant.API_URL_PRODUCTS, params=payload)
        data = response.json()
        self._page_counter = self._page_counter + 1
        self._list_products = data['products']
        return len(self._list_products) > 0
