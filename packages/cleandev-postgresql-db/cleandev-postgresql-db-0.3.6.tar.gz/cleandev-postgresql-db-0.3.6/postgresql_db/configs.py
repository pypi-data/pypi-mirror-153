import os

from properties_loader import PropertiesImpl
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from properties_loader.interfaces import Properties
from postgresql_db.inmutables import _Groups, _Properties, _Config, _DDLOptions
from generic_utils import CleanDevGenericUtils

__utils = CleanDevGenericUtils()
__key: str = os.getenv('FERNET_KEY')

_properties: Properties = PropertiesImpl().__dict__

_db_properties: dict = _properties.get(_Groups.BD_CORE)
_ddl_auto_options: list = [
    str(_DDLOptions.CREATE),
    str(_DDLOptions.DROP_CREATE),
    str(_DDLOptions.TEST)
]

_config: dict = {
    str(_Config.DDL_AUTO_VALUE): _db_properties.get(_Properties.DDL_AUTO),
    str(_Config.NAME_SHCEMA_MODULE): _db_properties.get(_Properties.PATH_MODULE_SCHEMA)
}


def __get_url():
    _db_driver: str = _db_properties[_Properties.DB_DRIVER]
    _db_ip: str = _db_properties[_Properties.DB_IP]
    _db_port: str = _db_properties[_Properties.DB_PORT]
    _db_user: str = _db_properties[_Properties.DB_USER]
    _db_password: str = __utils.decrypt(_db_properties[_Properties.DB_PASSWORD], __key)
    _db_name: str = _db_properties[_Properties.DB_NAME]
    _url_connection: str = f'{_db_driver}{_db_user}:{_db_password}@{_db_ip}:{_db_port}/{_db_name}'
    return _url_connection


_url_connection: str = __get_url()
_engine = create_engine(_url_connection)

# Factoria de sessiones
StandardSession: Session = sessionmaker(_engine, autocommit=False)
AutoCommitSession: Session = sessionmaker(_engine, autocommit=True)
