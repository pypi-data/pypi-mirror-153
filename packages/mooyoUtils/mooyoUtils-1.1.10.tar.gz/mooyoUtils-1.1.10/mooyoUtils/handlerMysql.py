# -*- coding: UTF-8 -*-
# @Time     : 2020/8/27 11:00
# @Author   : Jackie
# @File     : handlerMysql.py

import pymysql

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .read_config import apollo_reader
from .logger import logger


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        # 通过 对象+参数 共同判断单例的唯一性
        _obj_key = '-'.join([str(cls), str(sorted(args)), str(sorted(kwargs.items()))])
        if _obj_key not in instances:
            instances[_obj_key] = cls(*args, **kwargs)
        return instances.get(_obj_key)

    return wrapper


@singleton
class MyDB:
    def __init__(self, database='default'):
        apollo_configurations = apollo_reader.get_configurations()
        mysql_hosts = [key for key in apollo_configurations.keys() if key.startswith('mysql') and key.endswith('host')]
        databases = [database.split('.')[1] for database in mysql_hosts]

        self.database = database
        if self.database not in databases:
            self.database = 'default'

        db_config = {
            'host': apollo_reader.get_value('mysql.%s.host' % str(self.database)),
            'user': apollo_reader.get_value('mysql.%s.user' % str(self.database)),
            'passwd': apollo_reader.get_value('mysql.%s.pwd' % str(self.database)),
            'port': int(apollo_reader.get_value('mysql.%s.port' % str(self.database))),
            'db': apollo_reader.get_value('mysql.%s.database' % str(self.database)),
            'autocommit': True,
        }

        self.db = pymysql.connect(**db_config)
        self.cursor = self.db.cursor()
        self.cursor_dict = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def execute_sql(self, sql, is_dict=False, is_commit=True):
        self.ping()
        if is_dict:
            self.cursor_dict.execute(sql)
            cursor = self.cursor_dict
        else:
            self.cursor.execute(sql)
            cursor = self.cursor
        if is_commit:
            self.db.commit()
        return cursor

    def get_all(self, is_dict=False):
        if is_dict:
            value = self.cursor_dict.fetchall()
        else:
            value = self.cursor.fetchall()
        return value

    def get_one(self):
        value = self.cursor.fetchone()
        if value is not None:
            try:
                return value[0]
            except IndexError:
                return None
        return value

    def commit(self):
        self.db.commit()

    def ping(self, reconnect=True):
        self.db.ping(reconnect)

    def close_db(self):
        self.db.close()
        logger.info("Database closed!")


class DBManagerORM:

    def __init__(self) -> None:
        self.db_cache = {}

    def init_db(self, db_name):
        db_url = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4&' \
                 'autocommit={autocommit}'
        configurations = apollo_reader.get_configurations()
        mysql_hosts = [key for key in configurations.keys() if key.startswith('mysql') and key.endswith('host')]
        databases = [database.split('.')[1] for database in mysql_hosts]

        if db_name not in databases:
            db_name = 'default'

        db_setting = {
            'host': apollo_reader.get_value(f'mysql.{db_name}.host'),
            'port': apollo_reader.get_value(f'mysql.{db_name}.port'),
            'username': apollo_reader.get_value(f'mysql.{db_name}.user'),
            'password': apollo_reader.get_value(f'mysql.{db_name}.pwd'),
            'database': apollo_reader.get_value(f'mysql.{db_name}.database'),
            'autocommit': 'true',
        }
        db_url = db_url.format(**db_setting)
        if db_name not in self.db_cache:
            engine = create_engine(db_url, echo=False, max_overflow=5)
            session = sessionmaker(bind=engine)()
            self.db_cache[db_name] = session
        return self.db_cache[db_name]

    def close_db(self):
        for _, db in self.db_cache.items():
            db.disconnect()
        self.db_cache = {}

    def get_db(self, db_name):
        if db_name in self.db_cache:
            return self.db_cache[db_name]
        return self.init_db(db_name)


class DBManager:
    def __init__(self) -> None:
        self.db_cache = {}

    def init_db(self, db_name) -> MyDB:
        if db_name not in self.db_cache:
            self.db_cache[db_name] = MyDB(database=db_name)
        return self.db_cache[db_name]

    def close_db(self):
        for _, db in self.db_cache.items():
            db.close_db()
        self.db_cache = {}

    def get_db(self, db_name):
        if db_name in self.db_cache:
            return self.db_cache[db_name]
        return self.init_db(db_name)


db_manager_orm = DBManagerORM()
db_manager = DBManager()
