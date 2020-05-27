from core.dbconnector import DbConnector

class DaoProduct:

    def __init__(self):
        self.db = DbConnector()
        self.cnx = self.db.handle

    def get_product(self, id):
        """
        get a product id from his id
        :param id: identifiant
        :return: object product
        """
        cursor =  self.cnx.cursor()
        cursor.execute('SELECT id FROM Product WHERE id = %s', (id,))
        prod_id = cursor.fetchone()
        cursor.close()
        return None if prod_id is None else prod_id[0]