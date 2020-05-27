# -*- coding: utf-8 -*- #
from core import constant


class Product():
    """Classe permettant de créer un product """



    """ product constructor """
    def __init__(self,  **product):
        self._columns_values = dict()
        self._columns_values['ean_code'] = product['code']
        self._columns_values['product_name'] = product['product_name']
        self._columns_values['generic_name'] = product['generic_name_fr']
        self._columns_values['brands'] = product['brands']
        self._columns_values['stores'] = product['stores']
        self._columns_values['url'] = product['url']
        self._columns_values['nutrition_grade'] = product['nutrition_grade_fr']
        self._columns_names =['ean_code', 'product_name', 'generic_name', 'brands', 'stores', 'url', 'nutrition_grade']

    #TODO faire builder avec @classmethod

    @property
    def id(self):
        return self._id

    @property
    def ean_code(self):
        return self._ean_code

    @property
    def name(self):
        return self._name

    @property
    def generic_name(self):
        return self._generic_name

    @property
    def brands(self):
        return self._brands

    @property
    def stores(self):
        return self._stores

    @property
    def url(self):
        return self._url

    @property
    def nutrition_grade(self):
        return self._nutrition_grade

    @property
    def columns_names(self):
        return self._columns_names

    @property
    def columns_values(self):
        return self._columns_values
