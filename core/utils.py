"""argument parsing """
import argparse
import logging as lg
from sys import (stdout)

logger = lg.getLogger(__name__)


def parse_arguments(argv=None):
    """Parse_arguments parsing args
     parameters :
        --datafile : name of file map without extension """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--nbcategory", help=""" Maximum categories number
        """, default="10")
    parser.add_argument("-c", "--country", help=""" Country where data are selected from
        """, default='France')
    parser.add_argument("-n", "--nbproducts", help="""  Maximum products number
        """, default="100000")
    parser.add_argument("-gpi", "--get_product_by_id", help="""  Get product object by id
        """, default="0")
    parser.add_argument("-gci", "--get_category_by_id", help="""  Get category object by id
        """, default="0")
    parser.add_argument("-gcl", "--get_category_list", help="""  Get category list
        """, action="store_true")
    parser.add_argument("-gplc", "--get_product_list_by_category_id",
                        help="""  Get product list by category_id""", default="")
    parser.add_argument("-gpsl", "--get_products_subst_list",
                        help="""  Get product subsitute list by id""", default="0")
    parser.add_argument("-gplm", "--get_products_list_by_match",
                        help="""  Get product by match on key words
        between the names of products or categories. Wildcad '*' is allowed.
        """, default="")
    parser.add_argument("-ssp", "--set_substitute_product",
                        help="""  Set relation product,substitute by id""", default="")
    parser.add_argument("-r", "--reload", help="Reload database from Openfactsfood services",
                        action="store_true")
    # si on argv est passé en parametre
    # on checke si les arguments sont présents
    if argv is not None and len(argv) == 1:
        parser.print_usage()

    return parser.parse_args()


def set_logger():
    """set log environement."""
    # Set logging stuff
    # logger
    file_handle = lg.StreamHandler(stdout)
    formatter = lg.Formatter('%(asctime)s - %(levelname)s -'
                             ' %(filename)s - %(funcName)s - %(message)s')
    file_handle.setFormatter(formatter)
    logger = lg.getLogger()

    logger.addHandler(file_handle)
    logger.setLevel(lg.DEBUG)
