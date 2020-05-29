# -*- coding: utf-8 -*- #


class Category:
    """Classe permettant de créer une category """

    """ category constructor """

    def __init__(self, **category):
        # petite verrue l'attribut id de off est renommé en id_off
        self._columns_values = dict()
        self._columns_values['id_off'] = category['id'] if 'id' in category else None
        self._columns_values['url'] = category['url'] if 'url' in category else None
        self._columns_values['name'] = category['name'] if 'name' in category else None
        self._columns_names = ['id_off', 'url', 'name']

    # builder json
    @classmethod
    def buildfromjson(cls, **category):
        return cls(**category)

    # builder mysql
    @classmethod
    def buildfrommysql(cls, **category):
        return cls(**category)

    def __str__(self):
        return str(self._columns_values)

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
