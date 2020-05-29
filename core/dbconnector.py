# -*- coding: utf-8 -*- #

from core import constant
import json
import mysql.connector

class DbConnector:

    def __init__(self, pathcfg = constant.DB_CONFIG_FILE):
        """ Init 1 connexion/session pour 1 objet DbConnector instancié """
        with open(pathcfg) as f:
            self._handle = mysql.connector.connect(
                **json.load(f)
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
