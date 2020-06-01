from core.dbconnector import DbConnector
from core.model.category import Category


class DaoCategory:

    def __init__(self):
        self.db = DbConnector()
        self.cnx = self.db.handle

    def get_category_id(self, id_off):
        """
        get a category id from his tag
        :param cnx: cnx handle
        :param id_off: id openfoodfacts
        :return: Category
        """
        cursor = self.cnx.cursor()
        cursor.execute('SELECT id FROM Category WHERE id_off = %s', (id_off,))
        cat_id = cursor.fetchone()
        cursor.close()
        return None if cat_id is None else cat_id[0]

    def get_category_by_id(self, ident):
        """
        get a category object by his id
        :param id: pk
        :return: category product
        """
        category = None
        cursor = self.cnx.cursor()
        cursor.execute('SELECT * FROM Category WHERE id = %s', (ident,))
        a_row = cursor.fetchone()
        if a_row:
            map_row = dict(zip(cursor.column_names, a_row))
            category = Category.buildfrommysql(**map_row)
        cursor.close()
        return category


    def get_category_list(self, limit=100):
        """
        get a list of categorie (w.o condition)
        :return: list json of categories
        """

        # list 2 return
        categories_list = list()

        cursor = self.cnx.cursor()

        # 1rst call we must determine string comparison
        comp_req = "SELECT * from category"

        cursor.execute(comp_req)

        for a_row in cursor:
            map_row = dict(zip(cursor.column_names, a_row))
            categories_list.append(Category.buildfrommysql(**map_row))

        cursor.close()
        return categories_list
