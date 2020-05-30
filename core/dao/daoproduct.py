"""DaoProduct
This class allows access to product data

"""
from core.dbconnector import DbConnector
from core.model.product import Product


class DaoProduct:
    """ DaoProduct """
    def __init__(self):
        """ DaoProduct needs active cnx
         to be functional"""
        self.database = DbConnector()
        self.cnx = self.database.handle

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

    def get_product_by_id(self, ident):
        """
        get a product object from his id
        :param id: pk
        :return: object product
        """
        product = None
        cursor = self.cnx.cursor()
        cursor.execute('SELECT * FROM Product WHERE id = %s', (ident,))
        a_row = cursor.fetchone()
        if a_row:
            map_row = dict(zip(cursor.column_names, a_row))
            product = Product.buildfrommysql(**map_row)
        cursor.close()
        return product

    def get_product_list_by_category_id(self, category_id, limit=100):
        """
        get a product object from his category_id
        :param limit:
        :param category_id:
        :param id: pk
        :return: object product list
        """
        # list 2 return
        products_list = list()

        cursor = self.cnx.cursor()
        cursor.execute("SELECT * FROM Product P" \
                       "    INNER JOIN ProductCategory PC ON P.id = PC.product_id" \
                       " WHERE PC.category_id = %s" \
                       " LIMIT  " + str(limit)
                       , (category_id,))

        for a_row in cursor:
            map_row = dict(zip(cursor.column_names, a_row))
            products_list.append(Product.buildfrommysql(**map_row))

        cursor.close()

        return None if category_id is None else products_list

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
                    "       MATCH (P.`product_name`" \
                    "           ,P.`generic_name`,P.`brands`) " \
                    "           AGAINST ('%s' in BOOLEAN MODE) " \
                    "       OR " \
                    "           MATCH (C.`name`) AGAINST ('%s' in BOOLEAN MODE) " \
                    "LIMIT  " + str(limit)

        cursor.execute(final_req % (match_keys, match_keys))

        for a_row in cursor:
            map_row = dict(zip(cursor.column_names, a_row))
            products_list.append(Product.buildfrommysql(**map_row))

        cursor.close()
        return None if id is None else products_list

    def get_products_subst_list_by_id(self, ident, limit=100):
        """
        get a substitute product list from  id product
        :param id:  id of product to match
        :return: list json of products
        """

        # list 2 return
        products_list = list()

        cursor = self.cnx.cursor()

        # 1rst call we must determine string comparison
        comp_req = "SELECT concat(`product_name`,' ',`generic_name`,' ',`brands`)" \
                   " FROM Product WHERE id = '%s'"

        cursor.execute(comp_req, (ident,))
        comp_str = cursor.fetchone()
        escaped_str = (comp_str[0]).replace("'", " ")

        if comp_str is not None:
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
                        "                SELECT category_id " \
                        "                   FROM ProductCategory " \
                        "                WHERE Product_id = %s)" \
                        "        GROUP BY product_id" \
                        "       ) AS Subst" \
                        "    INNER JOIN product AS P ON Subst.product_id = P.id" \
                        "    INNER JOIN Category AS C ON Subst.category_id = C.id" \
                        "    WHERE P.nutrition_grade < (" \
                        "       SELECT nutrition_grade FROM Product WHERE id = %s" \
                        "       )" \
                        "ORDER BY nb_shared_categories DESC, nutrition_grade, score desc " \
                        "LIMIT  " + str(limit)

            cursor.execute(final_req % (escaped_str, ident, ident))

        for a_row in cursor:
            map_row = dict(zip(cursor.column_names, a_row))
            products_list.append(Product.buildfrommysql(**map_row))

        cursor.close()
        return None if id is None else products_list
