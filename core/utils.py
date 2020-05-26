import argparse
import logging as lg
import sys
from sys import (stdout, path)

logger = lg.getLogger(__name__)


def parse_arguments():
    """Parse_arguments parsing args
     parameters :
        --datafile : name of file map without extension """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--nbcategory", help=""" Maximum categories number
        """, default="10")
    parser.add_argument("-c", "--country", help=""" Country where data are selected from 
        """, default='France')
    parser.add_argument("-i", "--nbcproducts", help="""  Maximum products number
        """, default="100000")
    return parser.parse_args()


def set_logger():
    """set log environement."""
    # Set logging stuff
    fh = lg.StreamHandler(stdout)
    formatter = lg.Formatter('%(asctime)s - %(levelname)s -'
                             ' %(filename)s - %(funcName)s - %(message)s')
    fh.setFormatter(formatter)
    logger = lg.getLogger()

    logger.addHandler(fh)
    logger.setLevel(lg.DEBUG)

