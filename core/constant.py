# -*- coding: utf-8 -*- #
# limite nb de produits par catégorie
# (en dessous de laquelle on ne charge pas les produits attachés)
LOW_LIMIT_NB_PRODUCTS = 10000
# default nb de catégories max à charger (overlaps LOW_LIMIT_NB_PRODUCTS)
LIMIT_NB_CATEGORIES = 20
# default country origin
DEFAULT_COUNTRY_ORIGIN = "France"
# service API url for categories
API_URL_CATEGORIES = "https://fr.openfoodfacts.org/products/categories"
# service API url for categories
API_URL_PRODUCTS = "https://fr.openfoodfacts.org/cgi/search.pl"
# default nb de produits  max à charger (chunk size)
LIMIT_NB_PRODUCTS = 1000
# default db config file
DB_CONFIG_FILE = 'resources/database.json'
