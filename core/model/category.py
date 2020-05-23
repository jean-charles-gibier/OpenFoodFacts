# -*- coding: utf-8 -*- #
from core import constant


class Category:
    """Classe permettant de créer une category """


    """ category constructor """
    def __init__(self, **category):
        # petite verrue l'attribut id est renommé en tag
        self._columns_values = dict()
        self._columns_values['tag'] = category['id']
        self._columns_values['url'] = category['url']
        self._columns_values['name'] = category['name']
        self._columns_names=['tag', 'url', 'name']

    @property
    def id(self):
        return self._id

    @property
    def tag(self):
        return self._tag

    @property
    def name(self):
        return self._name

    @property
    def columns_names(self):
        return self._columns_names

    @property
    def columns_values(self):
        return self._columns_values
