# -*- coding: utf-8 -*- #
import json

import mysql
from core.dao.database import Database


"""


    Immediately before the first statement, determine the highest ROWID in use in the table.

    oldmax ← Execute("SELECT max(ROWID) from nodes").

    Perform the first insert as before.

    Read back the row IDs that were actually assigned with a select statement:

    NewNodes ← Execute("SELECT ROWID FROM nodes WHERE ROWID > ? ORDER BY ROWID ASC", oldmax) .

    Construct the connection_values array by combining the parent ID from new_values and the child ID from NewNodes.

    Perform the second insert as before.

"""
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
        db = Database()
        cnx = db.handle
        cursor = cnx.cursor()
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
        cnx.commit()
        cnx.close()
