from core.dbconnector import DbConnector
from core.model.product import Product


class DaoProduct:

    def __init__(self):
        self.db = DbConnector()
        self.cnx = self.db.handle

    def get_id_product_by_ean(self, ean):
        """
        get a product id from his ean code
        :param ean: identifiant ean
        :return: object product
        """
        cursor = self.cnx.cursor()
        cursor.execute('SELECT id FROM Product WHERE ean_code = %s', (ean,))
        prod_id = cursor.fetchone()
        cursor.close()
        return None if prod_id is None else prod_id[0]

    def get_product_by_id(self, id):
        """
        get a product objetc from his id
        :param id: pk
        :return: object product
        """
        cursor = self.cnx.cursor()
        cursor.execute('SELECT * FROM Product WHERE id = %s', (id,))

        map_row = dict(zip(cursor.column_names, cursor.fetchone()))
        product = Product.buildFromMysql(**map_row)
        cursor.close()

        return None if id is None else product

    def get_products_list_by_match(self, match_keys, limit=100):
        """
        get a substitute product list from  id product
        :param match_keys: string that contains key words to find
        :return: list json of products
        """

        # list 2 return
        products_list = list()

        cursor = self.cnx.cursor()

        final_req = "select P.* from Product P " \
                    "inner join ProductCategory PC on PC.product_id = P.id " \
                    "        inner join Category C on PC.category_id = C.id " \
                    "WHERE " \
                    "                            MATCH (P.`product_name`,P.`generic_name`,P.`brands`) " \
                    "                            AGAINST ('%s' in BOOLEAN MODE) " \
                    "                    OR " \
                    "                            MATCH (C.`name`) AGAINST ('%s' in BOOLEAN MODE) " \
                    "LIMIT  " + str(limit)

        cursor.execute(final_req % (match_keys, match_keys))

        for a_row in cursor:
            map_row = dict(zip(cursor.column_names, a_row))
            products_list.append(Product.buildFromMysql(**map_row))

        cursor.close()
        return None if id is None else products_list

    def get_products_subst_list_by_id(self, id, limit=100):
        """
        get a substitute product list from  id product
        :param id:  id of product to match
        :return: list json of products
        """

        # list 2 return
        products_list = list()

        cursor = self.cnx.cursor()

        # 1rst call we must determine string comparison
        comp_req = "SELECT  concat(`product_name`,' ',`generic_name`,' ',`brands`)" \
                   " FROM Product WHERE id = '%s'"

        cursor.execute(comp_req, (id,))
        comp_str = cursor.fetchone()

        final_req = "select  P.*, nb_shared_categories ," \
                    "MATCH (P.`product_name`,P.`generic_name`,P.`brands`) AGAINST (" \
                    "       '%s'" \
                    "  IN NATURAL LANGUAGE MODE) AS score" \
                    "    FROM (" \
                    "        SELECT" \
                    "            product_id," \
                    "            COUNT(product_id) AS nb_shared_categories," \
                    "            category_id" \
                    "        FROM" \
                    "           ProductCategory PC2" \
                    "            INNER JOIN Category AS C2 ON PC2.category_id = C2.id " \
                    "            WHERE category_id IN (" \
                    "                SELECT category_id FROM ProductCategory WHERE Product_id = %s)" \
                    "        GROUP BY product_id" \
                    "       ) AS Subst" \
                    "    INNER JOIN product AS P ON Subst.product_id = P.id" \
                    "    INNER JOIN Category AS C ON Subst.category_id = C.id" \
                    "    WHERE P.nutrition_grade < (" \
                    "       SELECT nutrition_grade FROM Product WHERE id = %s" \
                    "       )" \
                    "ORDER BY nb_shared_categories DESC, nutrition_grade, score desc " \
                    "LIMIT  " + str(limit)

        cursor.execute(final_req % (comp_str[0], id, id))

        for a_row in cursor:
            map_row = dict(zip(cursor.column_names, a_row))
            products_list.append(Product.buildFromMysql(**map_row))

        cursor.close()
        return None if id is None else products_list
