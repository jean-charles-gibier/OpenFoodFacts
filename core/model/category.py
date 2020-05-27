# -*- coding: utf-8 -*- #
from core import constant


class Category:
    """Classe permettant de créer une category """


    """ category constructor """
    def __init__(self, **category):
        # petite verrue l'attribut id de off est renommé en id_off
        self._columns_values = dict()
        self._columns_values['id_off'] = category['id']
        self._columns_values['url'] = category['url']
        self._columns_values['name'] = category['name']
        self._columns_names=['id_off', 'url', 'name']

    @property
    def id(self):
        return None

    @property
    def id_off(self):
        return self._columns_values['id_off']

    @property
    def name(self):
        return self._columns_values['name']

    @property
    def columns_names(self):
        return self._columns_names

    @property
    def columns_values(self):
        return self._columns_values
