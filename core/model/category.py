# -*- coding: utf-8 -*- #
"""
category definition
"""


class Category:
    """ category constructor """

    def __init__(self, **category):
        # petite verrue l'attribut id de off est renommé en id_off
        self._columns_values = dict()
        self._columns_values['id'] = category['id'] if 'id' in category else None
        self._columns_values['id_off'] = category['id_off'] if 'id_off' in category else None
        self._columns_values['url'] = category['url'] if 'url' in category else None
        self._columns_values['name'] = category['name'] if 'name' in category else None
        self._columns_names = ['id_off', 'url', 'name']

    # builder json
    @classmethod
    def buildfromjson(cls, **category):
        """ data from json"""
        return cls(**category)

    # builder mysql
    @classmethod
    def buildfrommysql(cls, **category):
        """ data from mysql"""
        return cls(**category)

    def __str__(self):
        """ print category in std way """
        return "{:<30}: {}\n".format('Identifiant', str(self.ident)) + \
               "{:<30}: {}\n".format('Identifiant OFF', self.id_off) + \
               "{:<30}: {}\n".format('Nom', self.name) + \
               "{:<30}: {}\n".format('url', self.url)

    def list_item(self, print_header=False):
        """ print category in list way
         if print_header print header :-) """
        if print_header:
            print("{:<15}".format('Identifiant') +
                  "{:<25}".format('Identifiant OFF') +
                  "{:<30}".format('Nom') +
                  "{:<30}".format('url'))

        print("{:<15}".format(str(self.ident)) +
              "{:<25}".format(self.id_off) +
              "{:<30}".format(self.name) +
              "{:<30}".format(self.url))

    def print_json(self):
        """ print in json """
        return str(self._columns_values)

    @property
    def ident(self):
        """ should return id """
        return self._columns_values['id']

    @property
    def id_off(self):
        """ returns openfactsfood id """
        return self._columns_values['id_off']

    @property
    def name(self):
        """ returns off name """
        return self._columns_values['name']

    @property
    def url(self):
        """ returns off url """
        return self._columns_values['url']

    @property
    def columns_names(self):
        """ returns dict of names
        (each keys is the name of the element)"""
        return self._columns_names

    @property
    def columns_values(self):
        """ returns dict of values """
        return self._columns_values
