# -*- coding: UTF-8 -*-
# @Time     : 2020/7/10 10:22
# @Author   : Jackie
# @File     : handlerMongo.py
from .logger import logger
import pymongo


class MongoHandler:
    def __init__(self, conn_config):
        self.client = pymongo.MongoClient(conn_config)
        self.dbs = {}
        self.coll_list = {}
        logger.info(f'MongoClient conn success. {self.client}')

    def get_db(self, db_name):
        if db_name in self.dbs:
            return self.dbs[db_name]['obj']
        db = self.client.get_database(db_name)
        self.dbs[db_name] = {}
        self.dbs[db_name]['obj'] = db
        return db

    def get_coll(self, db_name, coll_name):
        db = self.get_db(db_name)
        db_data = self.dbs[db_name]
        if coll_name in db_data:
            return db_data[coll_name]
        coll = db[coll_name]
        db_data[coll_name] = coll
        return coll

    def get_result(self, db_name, coll_name, params, *args, **kwargs):
        logger.info(f'Query mongo: db_name:{db_name}, coll_name:{coll_name}, params:{args, kwargs}')
        coll = self.get_coll(db_name, coll_name)
        return list(coll.find(params, *args, **kwargs))


if __name__ == '__main__':
    m = MongoHandler('mongodb://root:5T8JbklD9v5ylAZ@s-d9j40f279e3cd0c4.mongodb.ap-southeast-5.rds.aliyuncs.com:3717,s-d9jc65211d9803b4.mongodb.ap-southeast-5.rds.aliyuncs.com:3717/sdk-backend?authSource=admin')
    print(m.client.get_database('userData'))
    r = m.get_result('userData', 'user', {'user_id': 100})
    print(r)
