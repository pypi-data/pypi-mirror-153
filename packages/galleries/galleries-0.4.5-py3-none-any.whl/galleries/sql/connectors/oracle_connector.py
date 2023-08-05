import cx_Oracle
from propsettings.configurable import register_as_setting
from propsettings.setting_types.password_setting_type import Password

from galleries.sql.connectors import GallerySqlConnector


class OracleConnector(GallerySqlConnector):

    def __init__(self, username: str = "", password: str = "", dsn: str = "", port: int = 1512, encoding='UTF-8'):
        self._username = username
        self._password = password
        self._dsn = dsn
        self._port = port
        self._encoding = encoding

    def connect(self):
        connection = cx_Oracle.connect(
            self._username,
            self._password,
            self._dsn,
            encoding=self._encoding)
        return connection


register_as_setting(OracleConnector, "_username", setting_value_type=str, sort_order=0)
register_as_setting(OracleConnector, "_password", setting_value_type=str, setting_type=Password(), sort_order=1)
register_as_setting(OracleConnector, "_dsn", setting_value_type=str, sort_order=2)
register_as_setting(OracleConnector, "_port", setting_value_type=int, sort_order=3)
register_as_setting(OracleConnector, "_encoding", setting_value_type=str, sort_order=4)
