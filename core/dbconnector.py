# -*- coding: utf-8 -*- #
"""
Connection stuff
 mysql connector
"""
import json
import mysql.connector
from core import constant


class DbConnector(object):
    """ un instance = un handle"""
    def __init__(self, pathcfg=constant.DB_CONFIG_FILE):
        """ Init 1 connexion/session pour 1 objet DbConnector instancié """
        with open(pathcfg) as file_cfg:
            self._handle = mysql.connector.connect(
                **json.load(file_cfg)
            )

    def __del__(self):
        """ Au cas où """
        if hasattr(self, '_handle'):
            self._handle.close()
            delattr(self, '_handle')

    @property
    def handle(self):
        """ identifiant de session  """
        return self._handle
