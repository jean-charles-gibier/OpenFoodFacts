# -*- coding: utf-8 -*- #
import logging as lg
import sys

import mysql

from core.dbconnector import DbConnector

logger = lg.getLogger(__name__)


class Writer:
    """
    Writer is a mapping substitution
    it is used for raw insertion
    """
    """ cf  build_raw_request for explanations """
    PLACEHOLDER_MODE = 1
    INLINE_MODE = 2

    def __init__(self, table_name):
        """ init element list """
        self._bulk_list = list()
        """ table name """
        self._table_name = table_name
        """ insert (ignore) pattern """
        self._raw_insert_ignore_pattern = "insert ignore into %s %s values %s %s"
        """ request raw insertion """
        self._raw_insert_ignore_request = ""
        """ columns names for insert """
        self._columns_names = ""
        """ columns values for insert """
        self._values_list = ""

    def add_row(self, row_element):
        """ add a row element to be writen """
        if type(row_element) is dict:
            self._bulk_list.append(row_element['columns_values'])
            if not self._columns_names:
                self._columns_names = row_element['columns_names']
        else:
            # object model
            self._bulk_list.append(row_element.columns_values)
            if not self._columns_names:
                self._columns_names = row_element.columns_names

    def add_rows(self, json_list, zcls):
        """ add a bunch of rows
        json_list :
        zcls : can be a class type or an dict
        """
        for idx, some in enumerate(json_list):
            try:
                # we get dict values
                if isinstance(zcls, dict):
                    transf = self.make_writable(some, zcls)
                    self.add_row(transf)
                # we get object (Category, Product)
                else:
                    an_instance = zcls(**some)
                    self.add_row(an_instance)
            except:
                json_list.pop(idx)
                logger.error('[%s] Ne peut enregistrer #%s', sys.exc_info()[0], str(some))

        return json_list

    def _build_raw_request(self, mode):
        """ build insert request
        mode :
        1 : PLACEHOLDER_MODE => requête 'executemany' avec placeholder "python_connector"
        2 : INLINE_MODE "sql natif" => requête 'execute' avec sql standard (requête "in extenso")
        """
        columns_names = ', '.join(self._columns_names)
        columns_names = '(' + columns_names + ')'
        on_duplicate = ''

        if mode == self.PLACEHOLDER_MODE:
            values_list = ', '.join(['%(' + col_name + ')s' for col_name in self._columns_names])
            values_list = '(' + values_list + ')'
        else:
            values_list = ', '.join(
                ["((select id from product where ean_code ='" + values["product_id"] + "'), " + str(
                    values["category_id"]) + ")" for values in self._bulk_list])
        self._raw_insert_ignore_request = self._raw_insert_ignore_pattern % (
            self._table_name, columns_names, values_list, on_duplicate)

    def write_rows(self):
        """ write specified values in specified table """
        self._build_raw_request(self.PLACEHOLDER_MODE)
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
        """ write simple jointure many 2 many table """
        self._build_raw_request(self.INLINE_MODE)
        db = DbConnector()
        cnx = db.handle
        cursor = cnx.cursor()

        try:
            cursor.execute(
                self._raw_insert_ignore_request
            )
        except mysql.connector.Error as err:
            print("Failed inserting database: {}".format(err))

        # vide la liste qui vient d'être écrite
        self._bulk_list.clear()

        cursor.close()
        cnx.commit()
        cnx.close()

    def make_writable(self, infos, zcls):
        """ prepare un objet insérable pour Writer """
        ncls = dict(zcls)
        for k in ncls.keys():
            if isinstance(ncls[k], str) and ncls[k].startswith('$'):
                ncls[k] = infos[ncls[k][1:]]
        return {
            "columns_values": ncls,
            "columns_names": ncls.keys()
        }
