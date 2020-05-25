#!/usr/bin/python3
# coding: utf-8

import sys
from core import utils
from core import constant
from core.dao.daocategory import DaoCategory
from core.downloader.categorydownloader import CategoryDownloader
from core.downloader.productdownloader import ProductDownloader
from core.model.category import Category
from core.model.product import Product
from core.dao.writer import Writer

import logging as lg

logger = lg.getLogger(__name__)


def main():
    # prepare les logs
    utils.set_logger()
    # instance de chargement des catégories
    category_downloader = CategoryDownloader()

    if not category_downloader.fetch('France', constant.LIMIT_NB_CATEGORIES):
        raise Exception ("No category found : Abort.")
    # TODO ranger nb_categories dans category_downloader
    nb_categories = len(category_downloader.list_categories)
    logger.debug('Il y a %d categories à charger.', nb_categories)
    category_writer = Writer("category")
    product_writer = Writer("product")
    product_category_writer = Writer("productcategory")

    product_downloader = ProductDownloader()
    logger.debug('Start collecting categories')

    for category in category_downloader.list_categories:

        # record the current category
        try:
            a_category = Category(**category)
            category_writer.add_row(a_category)
        except:
            logger.error('[%s] Ne peut enregistrer #%s', sys.exc_info()[0], category)

    logger.debug('End collecting categories')

    logger.debug('Start writing categories')
    category_writer.write_rows()
    logger.debug('End writing categories')

    logger.debug('Start collecting products')
    for category in category_downloader.list_categories:
        product_downloader.reset_page_counter()
        dao_category = DaoCategory()
        id_category = dao_category.get_category_id(category['id'])

# boucle pour insertion produit
        while product_downloader.fetch(category['name'], constant.LIMIT_NB_PRODUCTS):
            logger.debug('Start getting page #%d', product_downloader.page_counter - 1)

            for product in product_downloader.list_products:
                try:
                    a_product = Product(**product)
                    product_writer.add_row(a_product)
                except :
                    logger.error('[%s] Ne peut enregistrer #%s', sys.exc_info()[0], product)

                # informations jointure

                try:
                    product_category_writer.add_row(
                        {"columns_values": {"product_id": product['code'],
                                            "category_id": id_category},
                         "columns_names":  ["product_id", "category_id"]}
                    )
                except :
                    logger.error('[%s] Ne peut enregistrer la jointure %s <=> %d', sys.exc_info()[0], product['code'], id_category)


            logger.debug('End getting page #%d', product_downloader.page_counter - 1)

            logger.debug('Start writing products')
            product_writer.write_rows()
            logger.debug('End writing products')
            logger.debug('Start writing product_category relations')
            product_category_writer.join_rows()
            logger.debug('End writing product_category relations')

    logger.debug('End collecting products')



if __name__ == "__main__":
    main()
