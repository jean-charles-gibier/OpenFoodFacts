# -*- coding: utf-8 -*- #

import mysql
from core.dbconnector import DbConnector


"""
    pour chaque categorie
        categorie => id de categorie courrante (en dur quoi)
        produit     => select id_product where ean_code = product code

"""
class Writer:

    """ pattern raw insertion """
    _raw_insert_ignore_pattern = "insert ignore into %s %s values %s %s"
    """ request raw insertion """
    _raw_insert_ignore_request = ""
    """ columns names for insert """
    _columnns_names = None
    """ columns values for insert """
    _values_list = ""
    """ table name """
    _table_name = ""


    def __init__(self,  table_name):
        """ init element list """
        self._bulk_list = list()
        self._table_name = table_name

    def add_row(self, row_element):
        """ TODO """
        if (type(row_element) is dict):
            self._bulk_list.append(row_element['columns_values'])
            if not self._columnns_names:
                self._columnns_names = row_element['columns_names']
        else:
            # object model
            self._bulk_list.append(row_element.columns_values)
            if not self._columnns_names:
                self._columnns_names = row_element.columns_names

    def _build_raw_request(self, mode):
        """ build insert request
        mode :
        1 : "python_connector" => requête 'executemany' avec placeholder
        2 : "sql natif" => requête 'execute' sql standard in extenso
        """
        columns_names = ', '.join(self._columnns_names)
        columns_names = '(' + columns_names + ')'
        on_duplicate = ''

        if mode == 1:
            values_list = ', '.join(['%(' + col_name + ')s' for col_name in self._columnns_names])
            values_list = '(' + values_list + ')'
        else:
            values_list = ', '.join(
                ["((select id from product where ean_code ='" + values["product_id"] + "'), " + str(values["category_id"] )+ ")" for values in self._bulk_list])

        self._raw_insert_ignore_request = self._raw_insert_ignore_pattern % (self._table_name, columns_names, values_list, on_duplicate)


    def write_rows(self):
        """ write specified values in specified table """
        self._build_raw_request(1)
        db = DbConnector()
        cnx = db.handle
        cursor = cnx.cursor()

        # exclusivité en écriture pour assurer une suite cohérente d'id autoincrementés
        cursor.execute('LOCK TABLES {} WRITE'.format(self._table_name))

        try:
            cursor.executemany(
                self._raw_insert_ignore_request, self._bulk_list
            )
        except mysql.connector.Error as err:
            print("Failed inserting database: {}".format(err))

        # vide la liste qui vient d'être écrite
        self._bulk_list.clear()

        cursor.execute('UNLOCK TABLES')
        cursor.close()
        cnx.commit()
        cnx.close()



    def join_rows(self):
        """ write simple many 2 many jointure """
        self._build_raw_request(2)
        db = DbConnector()
        cnx = db.handle
        cursor = cnx.cursor()

        # exclusivité en écriture pour assurer une suite cohérente d'id autoincrementés
#        cursor.execute('LOCK TABLES {} WRITE'.format(self._table_name))

        try:
            cursor.execute(
                self._raw_insert_ignore_request
            )
        except mysql.connector.Error as err:
            print("Failed inserting database: {}".format(err))

        # vide la liste qui vient d'être écrite
        self._bulk_list.clear()

 #       cursor.execute('UNLOCK TABLES')
        cursor.close()
        cnx.commit()
        cnx.close()
