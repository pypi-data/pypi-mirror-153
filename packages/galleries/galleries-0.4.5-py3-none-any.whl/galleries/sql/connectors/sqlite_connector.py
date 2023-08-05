from propsettings.configurable import register_as_setting
import sqlite3

from propsettings.setting_types.path_setting_type import Path

from galleries.sql.connectors import GallerySqlConnector


class SqliteConnector(GallerySqlConnector):

    def __init__(self, database_path: str = ""):
        self._database_path = database_path

    def connect(self):
        return sqlite3.connect(self._database_path)


register_as_setting(SqliteConnector, "_database_path", setting_type=Path(False, []))
