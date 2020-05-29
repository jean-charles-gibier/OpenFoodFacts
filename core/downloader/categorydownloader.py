import logging as lg
import sys

from core import constant

logger = lg.getLogger(__name__)


class CategoryDownloader:
    """ defines category object"""

    # a list of category id_off
    _list_categories = []

    @property
    def list_categories(self):
        """ get page counter """
        return self._list_categories

    @property
    def nb_categories(self):
        return len(self._list_categories)

    def fetch(self, origin=constant.DEFAULT_COUNTRY_ORIGIN, number=constant.LIMIT_NB_CATEGORIES,
              lower_limit=constant.LOW_LIMIT_NB_PRODUCTS):
        """fetch  downloads categories from OFF API
        origin : pays d'origine des relevés
        number : nombre de relevés
        lower_limit : nombre de produits minimum pour selectionner la categorie
        """
        import core.downloader.customrequest

        payload = {
            "origins": origin,
            "page_size": number,
            "page": 1,
            "json": 1,
        }

        try:
            response = core.downloader.customrequest.special_get(constant.API_URL_CATEGORIES, payload)
            data = response.json()
            # on ne selectionne que les catégories avec un nombre "consequent" de produits
            self._list_categories = [categorie for categorie in data['tags'] if categorie["products"] > lower_limit]
        except:
            logger.error("Unexpected error:", sys.exc_info()[0])

        return len(self._list_categories) > 0
