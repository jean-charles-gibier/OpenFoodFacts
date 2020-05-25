from core.dbconnector import DbConnector

class DaoCategory:

    def __init__(self):
        self.db = DbConnector()
        self.cnx = self.db.handle

    def get_category_id(self, tag):
        """
        get a category id from his tag
        :param cnx: cnx handle
        :param tag: string tag
        :return: id
        """
        cursor =  self.cnx.cursor()
        cursor.execute('SELECT id FROM Category WHERE tag = %s', (tag,))
        cat_id = cursor.fetchone()
        cursor.close()
        return None if cat_id is None else cat_id[0]