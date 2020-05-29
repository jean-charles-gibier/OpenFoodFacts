# -*- coding: utf-8 -*- #


class Product():
    """ Product object """
    """ constructor """

    def __init__(self, **product):
        self._columns_values = dict()
        self._columns_values['id'] = product['id'] if 'id' in product else None
        self._columns_values['ean_code'] = product['code'] if 'code' in product else None
        self._columns_values['product_name'] = product['product_name'] if 'product_name' in product else None
        self._columns_values['generic_name'] = product['generic_name_fr'] if 'generic_name_fr' in product else None
        self._columns_values['brands'] = product['brands'] if 'brands' in product else None
        self._columns_values['stores'] = product['stores'] if 'stores' in product else None
        self._columns_values['url'] = product['url'] if 'url' in product else None
        self._columns_values['nutrition_grade'] = product[
            'nutrition_grade_fr'] if 'nutrition_grade_fr' in product else None
        self._columns_names = ['ean_code', 'product_name', 'generic_name', 'brands', 'stores', 'url', 'nutrition_grade']

    # builder json
    @classmethod
    def buildfromjson(cls, **product):
        return cls(**product)

    # builder mysql
    @classmethod
    def buildfrommysql(cls, **product):
        # get 1 map from 2 with different origins => fusion with key change
        translation = {'ean_code': 'code', 'generic_name': 'generic_name_fr', 'nutrition_grade': 'nutrition_grade_fr'}
        new_map = dict([((k in translation and (translation.get(k))) or k, v) for k, v in product.items()])
        return cls(**new_map)

    def __str__(self):
        return str(self._columns_values)

    @property
    def id(self):
        return self._columns_values['id']

    @property
    def ean_code(self):
        return self._columns_values['ean_code']

    @property
    def name(self):
        return self._columns_values['name']

    @property
    def generic_name(self):
        return self._columns_values['generic_name']

    @property
    def brands(self):
        return self._columns_values['brands']

    @property
    def stores(self):
        return self._columns_values['stores']

    @property
    def url(self):
        return self._columns_values['url']

    @property
    def nutrition_grade(self):
        return self._columns_values['nutrition_grade']

    @property
    def columns_names(self):
        return self._columns_values

    @property
    def columns_values(self):
        return self._columns_values
