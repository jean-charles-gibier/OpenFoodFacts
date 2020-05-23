import requests

from core import constant


class CategoryDownloader:
    """ defines category object"""

    # a list of category tags
    _list_categories = []

    @property
    def list_categories(self):
        """ get page counter """
        return self._list_categories

    def fetch(self, origin=constant.DEFAULT_COUNTRY_ORIGIN, number=constant.LIMIT_NB_CATEGORIES, lower_limit=constant.LOW_LIMIT_NB_PRODUCTS):
        """fetch  downloads categories from OFF API
        origin : pays d'origine des relevés
        number : nombre de relevés
        lower_limit : nombre de produits minimum pour selectionner la categorie
        """
        payload = {
            "origins": origin,
            "page_size": number,
            "page": 1,
            "json": 1,
        }

        response = requests.get(constant.API_URL_CATEGORIES, params=payload)
        data = response.json()
        # on ne selectionne que les catégories avec un nombre "consequent" de produits
        self._list_categories = [categorie for categorie in data['tags'] if categorie["products"] > lower_limit]
        return len(self._list_categories) > 0
