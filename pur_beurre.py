# coding: utf-8
"""Main module of pure-beurre application
This script acts as a service that answer to the "menu" client application.
By passing options on command line, differents requests may be answered with
 or without parameters.
They are described in the --help option of this script.
python3 ./pur_beurre.py --help
"""
# !/usr/bin/python3
from __future__ import print_function
import sys
import logging as lg
from core import utils
from core.dao.daocategory import DaoCategory
from core.dao.daoproduct import DaoProduct
from core.filler import Filler


logger = lg.getLogger(__name__)


def main():
    """ main entry of this script
    see help option for more features description """
    args = utils.parse_arguments(sys.argv)
    # prepare les logs
    utils.set_logger()

    # option: chargement de la base
    if args.reload:
        Filler().start()
        sys.exit(0)

    if int(args.get_category_by_id) > 0:
        ident = int(args.get_category_by_id)
        dao_category = DaoCategory()
        search_category = dao_category.get_category_by_id(ident)
        if search_category is None:
            print("******************************************************")
            print("Pas de categorie trouvée pour cet identifiant")
            print("******************************************************")
        else:
            print("******************************************************")
            print("Vous cherchez le produit suivant :")
            print("******************************************************")
            print(search_category)
        sys.exit(0)

    if int(args.get_product_by_id) > 0:
        ident = int(args.get_product_by_id)
        dao_product = DaoProduct()
        search_product = dao_product.get_product_by_id(ident)
        if search_product is None:
            print("******************************************************")
            print("Pas de produit trouvé pour cet identifiant")
            print("******************************************************")
        else:
            print("******************************************************")
            print("Vous cherchez le produit suivant :")
            print("******************************************************")
            print(search_product)
        sys.exit(0)

    if int(args.get_products_subst_list) > 0:
        ident = int(args.get_products_subst_list)
        dao_product = DaoProduct()
        products = dao_product.get_products_subst_list_by_id(ident)
        search_product = dao_product.get_product_by_id(ident)
        print("******************************************************")
        print("Vous souhaitez un substitut pour le produit suivant :")
        print("******************************************************")
        print(search_product)
        print("******************************************************")
        print("Pur Beurre vous propose le substitut suivant :")
        print("******************************************************")
        for product in products:
            print(product)
        sys.exit(0)

    to_match = args.get_products_list_by_match
    if str(to_match) != "":
        dao_product = DaoProduct()
        products = dao_product.get_products_list_by_match(to_match)
        print("******************************************************")
        print("Résultat de la recherche sur les mots clés suivants :")
        print("******************************************************")
        print(to_match)
        print("******************************************************")
        print("Produits correspondants :")
        print("******************************************************")
        for product in products:
            print(product)
        sys.exit(0)

    category_id = args.get_product_list_by_category_id
    if str(category_id) != "":
        dao_product = DaoProduct()
        products = dao_product.get_product_list_by_category_id(category_id)
        print("******************************************************")
        print("Résultat de la recherche sur l'id categorie suivant:")
        print("******************************************************")
        print(category_id)
        print("******************************************************")
        print("Produits correspondants :")
        print("******************************************************")
        for product in products:
            print(product)
        sys.exit(0)

    if args.get_category_list:
        dao_category = DaoCategory()
        categories = dao_category.get_category_list()
        print("******************************************************")
        print("Résultat de la recherche sur les categories :")
        print("******************************************************")
        for category in categories:
            print(category)
        sys.exit(0)

    if args.get_recorded_substitutes_product:
        dao_product = DaoProduct()
        list_substitutes = dao_product.get_recorded_substitutes_product()
        print("******************************************************")
        print("Résultat des substitutions enregistrées (produit => substitut):")
        print("******************************************************")
        for substitute in list_substitutes:
            print(str(substitute))
        sys.exit(0)

    a_tuple = args.set_substitute_product
    if str(a_tuple) != "":
        r_tuple = tuple(str(a_tuple).split(','))
        Filler().set_substitute_product(r_tuple)
        print("******************************************************")
        print("Insertion de la substitution effectuée.")
        print("******************************************************")
        sys.exit(0)


if __name__ == "__main__":
    main()
