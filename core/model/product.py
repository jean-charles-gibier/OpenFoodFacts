# -*- coding: utf-8 -*- #
"""
product definition
"""


class Product():
    """ object constructor """

    def __init__(self, **product):
        self._columns_values = dict()
        self._columns_values['id'] = product['id'] \
            if 'id' in product else None
        self._columns_values['ean_code'] = product['code'] \
            if 'code' in product else None
        self._columns_values['product_name'] = product['product_name'] \
            if 'product_name' in product else None
        self._columns_values['generic_name'] = product['generic_name_fr'] \
            if 'generic_name_fr' in product else None
        self._columns_values['brands'] = product['brands'] \
            if 'brands' in product else None
        self._columns_values['stores'] = product['stores'] \
            if 'stores' in product else None
        self._columns_values['url'] = product['url'] \
            if 'url' in product else None
        self._columns_values['nutrition_grade'] = product[
            'nutrition_grade_fr'] \
            if 'nutrition_grade_fr' in product else None
        self._columns_names = \
            ['ean_code', 'product_name', 'generic_name',
             'brands', 'stores', 'url', 'nutrition_grade']

    def __str__(self):
        """ print product in std way """
        return "{:<30}: {}\n".format('Identifiant', str(self.ident)) + \
               "{:<30}: {}\n".format('Code ean', self.ean_code) + \
               "{:<30}: {}\n".format('Nom', self.name) + \
               "{:<30}: {}\n".format('Nom generique', self.generic_name) + \
               "{:<30}: {}\n".format('Marque', self.brands) + \
               "{:<30}: {}\n".format('Magasins', self.stores) + \
               "{:<30}: {}\n".format('Url', self.url) + \
               "{:<30}: {}\n".format('Grade', self.nutrition_grade)

    def list_item(self, print_header=False):
        """ print product in list way
         if print_header print header :-) """
        if print_header:
            print("{:<15}".format('Identifiant') +
                  "{:<30}".format('Nom') +
                  "{:<30}".format('Marque') +
                  "{:<5}".format('Grade'))

        print("{:<15}".format( str(self.ident)) +
              "{:<30}".format(self.name or '-') +
              "{:<30}".format(self.brands or '-') +
              "{:<5}".format(self.nutrition_grade or '-'))

    def print_json(self):
        """ print json way """
        return str(self._columns_values)

    # builder json
    @classmethod
    def buildfromjson(cls, **product):
        """ data from product """
        return cls(**product)

    # builder mysql
    @classmethod
    def buildfrommysql(cls, **product):
        """ data from mysql """
        # get 1 map from 2 with different origins => fusion with key change
        translation = {
            'ean_code': 'code',
            'generic_name': 'generic_name_fr',
            'nutrition_grade': 'nutrition_grade_fr'}
        new_map = dict([
            ((k in translation and (translation.get(k))) or k, v)
            for k, v in product.items()])
        return cls(**new_map)

    @property
    def ident(self):
        """ returns id product """
        return self._columns_values['id']

    @property
    def ean_code(self):
        """ returns barcode  """
        return self._columns_values['ean_code']

    @property
    def name(self):
        """ returns name """
        return self._columns_values['product_name']

    @property
    def generic_name(self):
        """ returns generic_name
        property openfactsfood """
        return self._columns_values['generic_name']

    @property
    def brands(self):
        """ returns brand names
        property openfactsfood """
        return self._columns_values['brands']

    @property
    def stores(self):
        """ returns store names
        property openfactsfood """
        return self._columns_values['stores']

    @property
    def url(self):
        """ returns url access
        property openfactsfood """
        return self._columns_values['url']

    @property
    def nutrition_grade(self):
        """ returns nutrition grade
        property openfactsfood """
        return self._columns_values['nutrition_grade']

    @property
    def columns_names(self):
        """ returns dict of names """
        return self._columns_names

    @property
    def columns_values(self):
        """ returns dict of values """
        return self._columns_values
