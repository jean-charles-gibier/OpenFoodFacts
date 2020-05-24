from core import constant
import json
import mysql.connector

class Database:

    def __init__(self, pathcfg = constant.DB_CONFIG_FILE):
        with open(pathcfg) as f:
            self._handle = mysql.connector.connect(
                **json.load(f)
                )

    def __del__(self):
        if hasattr(self, '_handle'):
            self._handle.close()

    @property
    def handle(self):
        return self._handle