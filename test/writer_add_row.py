import sys

sys.path.append('..')
sys.path.append('.')
import unittest


class MyTestCase(unittest.TestCase):
    def test_add_row(self):
        try:
            from core.dao.writer import Writer
            from core.model.product import Product
            writer = Writer("product")
            product = Product.buildfromjson(**{'nutrition_grade_fr': 'b',
                                               'url': 'https://fr.openfoodfacts.org/produit/3038359009051/le-kamalis-riz-parfume-premium-taureau-aile',
                                               'brands': 'Taureau ailé',
                                               'product_name': 'Le Kamâlis - Riz parfumé premium',
                                               'code': '3038359009051'})
            writer.add_row(product)
        except:
            print('[{}] Ne peut enregistrer #{}'.format(sys.exc_info()[0], "str(some)"))
            self.assertEqual(True, False)
        self.assertEqual(True, True)
        return 0


if __name__ == '__main__':
    unittest.main()
