# -*- coding: utf-8 -*- #
from core import constant
import mysql.connector


class Writer:

    """ pattern raw insertion """
    _raw_insert_ignore_pattern = "insert ignore into %s (%s) values (%s)"
    """ request raw insertion """
    _raw_insert_ignore_request = ""
    """ columns names for insert """
    _columnns_names = None
    """ columns values for insert """
    _values_list = ""
    """ table name """
    _table_name = ""


    def __init__(self,  table_name):
        """ element list """
        self._bulk_list = list()
        self._table_name = table_name

    def add_row(self, row_element):
        self._bulk_list.append(row_element.columns_values)
        if not self._columnns_names:
            self._columnns_names = row_element.columns_names

    def _build_raw_request(self):
        columns_names = ', '.join(self._columnns_names)
        values_list = ', '.join( [ '%(' + col_name + ')s' for col_name in self._columnns_names])
        self._raw_insert_ignore_request = self._raw_insert_ignore_pattern % (self._table_name, columns_names, values_list)

    def write_rows(self):
        self._build_raw_request()
        cnx = mysql.connector.connect(user='openfoodfacts', password='openfoodfacts',
                                     host='127.0.0.1',
                                     database='openfoodfacts_schema')
        cursor = cnx.cursor()
        try:
            cursor.executemany(
                self._raw_insert_ignore_request, self._bulk_list
            )
        except mysql.connector.Error as err:
            print("Failed inserting database: {}".format(err))

        # vide la liste qui vient d'être écrite
        self._bulk_list.clear()
        cnx.commit()
        cnx.close()

#    @property
#    def raw_insert_ignore_request(self):
#        self._build_raw_request()
#        return self._raw_insert_ignore_request
