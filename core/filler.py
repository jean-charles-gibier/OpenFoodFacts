# coding: utf-8

import logging as lg

from core import constant
from core.dao.daocategory import DaoCategory
from core.dao.writer import Writer
from core.downloader.categorydownloader import CategoryDownloader
from core.downloader.productdownloader import ProductDownloader
from core.model.category import Category
from core.model.product import Product

logger = lg.getLogger(__name__)


class Filler(object):
    """ classe en charge du chargement de la base """
    @classmethod
    def start(cls):
        """ unique mehode de chargement """
        # instance de chargement des catégories
        category_downloader = CategoryDownloader()
        # instance de chargement des produits
        product_downloader = ProductDownloader()

        if not category_downloader.fetch(constant.DEFAULT_COUNTRY_ORIGIN,
                                         constant.LIMIT_NB_CATEGORIES):
            raise Exception("No category found for {} : Abort."
                            .format(constant.DEFAULT_COUNTRY_ORIGIN))

        logger.debug('Il y a %d categories à charger.', category_downloader.nb_categories)
        category_writer = Writer("category")
        product_writer = Writer("product")
        product_category_writer = Writer("productcategory")

        logger.debug('Start collecting categories')
        category_writer.add_rows(category_downloader.list_categories, Category)
        logger.debug('End collecting categories')

        logger.debug('Start writing categories')
        category_writer.write_rows()
        logger.debug('End writing categories')

        # parcours des categories enregistrées
        logger.debug('Start collecting products')
        for category in category_downloader.list_categories:
            logger.debug('Start collecting category "%s"', category['name'])
            product_downloader.reset_page_counter()
            dao_category = DaoCategory()
            # get "our id" from "off id"
            category_id = dao_category.get_category_id(category['id'])

            # parcours des produits par catégories
            while product_downloader.fetch(category['name'], constant.LIMIT_NB_PRODUCTS):
                logger.debug('Start getting page #%d', product_downloader.page_counter - 1)
                # parcours des produits de la page courante
                new_list = product_writer.add_rows(product_downloader.list_products, Product)
                # ajout des index dans la table de jointure
                product_category_writer.add_rows(new_list,
                                                 {"product_id": '$code', "category_id": category_id})
                logger.debug('End collecting category "%s"', category['name'])
                # Ecriture en base
                logger.debug('Start writing products')
                product_writer.write_rows()
                logger.debug('End writing products')
                logger.debug('Start writing product_category relations')
                product_category_writer.join_rows(
                    "((select id from product where ean_code ='{{product_id}}')," +
                    "{{category_id}})")
                logger.debug('End writing product_category relations')

                logger.debug('End getting page #%d', product_downloader.page_counter - 1)
            logger.debug('End collecting category "%s"', category['name'])
        logger.debug('End collecting products')

    @classmethod
    def set_substitute_product(cls, pc_tuple):
        """  enregistre les liasons subistitut / produit """
        product_id, substitute_product_id = pc_tuple[0], pc_tuple[1]
        product_substitute = Writer("substitute")
        product_substitute.add_rows({1}, {"product_id": product_id,
                                          "substitute_product_id": substitute_product_id})
        product_substitute.write_rows()
