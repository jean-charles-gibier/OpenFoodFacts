# -*- coding: utf-8 -*- #
import mysql
from core.dbconnector import DbConnector


class Writer:
    """
    Writer is a mapping substitution
    it is used for raw insertion
    """
    """ cf  build_raw_request for explanations """
    INLINE_MODE = 0
    PLACEHOLDER_MODE = 1

    def __init__(self,  table_name):
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

    def _build_raw_request(self, mode):
        """ build insert request
        mode :
        1 : "PLACEHOLDER_MODE => requête 'executemany' avec placeholder "python_connector"
        2 : "sql natif" => requête 'execute' avec sql standard (requête "in extenso")
        """
        columns_names = ', '.join(self._columns_names)
        columns_names = '(' + columns_names + ')'
        on_duplicate = ''

        if mode == self.PLACEHOLDER_MODE:
            values_list = ', '.join(['%(' + col_name + ')s' for col_name in self._columns_names])
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
        """ write simple jointure many 2 many table """
        self._build_raw_request(2)
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
