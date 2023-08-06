# -*- coding: UTF-8 -*-
# @Time     : 2020/7/10 10:22
# @Author   : Jackie
# @File     : handlerRedis.py
import traceback

import redis
from .read_config import apollo_reader
from .logger import logger


class HandlerRedis:
    def __init__(self, tag=None):
        if not tag:
            self.config = {
                'host': apollo_reader.get_value('redis.host'),
                'port': int(apollo_reader.get_value('redis.port')),
                'password': apollo_reader.get_value('redis.password'),
                'db': apollo_reader.get_value('redis.db'),
                'decode_responses': True,
            }
        else:
            self.config = {
                'host': apollo_reader.get_value(f'redis.{tag}.host'),
                'port': int(apollo_reader.get_value(f'redis.{tag}.port')),
                'password': apollo_reader.get_value(f'redis.{tag}.password'),
                'db': apollo_reader.get_value(f'redis.{tag}.db'),
                'decode_responses': True,
            }

        self.default_ex = 3600 * 24
        self.pool = redis.ConnectionPool(**self.config)
        self.rds = redis.Redis(connection_pool=self.pool)
        self.pipe = self.rds.pipeline()
        logger.info('[%s] connected.' % self)

    def __str__(self):
        return 'Redis[{host}:{port}], db[{db}]'.format(**self.config)

    def set_ex(self, key, value, ex=3600*24):
        if ex == self.default_ex:
            ex = self.rds.ttl(key)
        if ex > 0:
            self.rds.setex(key, ex, value)
        else:
            self.rds.setex(key, self.default_ex, value)

    def lpush(self, key, data):
        self.rds.lpush(key, data)

    def llen(self, key):
        self.rds.llen(key)


class RedisHandler:
    """
    提供给主营的缓存操作工具
    """
    def __init__(self, host, port, password, db, *args, **kwargs):
        self.config = {
            'host': host,
            'port': port,
            'password': password,
            'db': db,
            'decode_responses': True,
        }
        self.args = args
        self.kwargs = kwargs
        self.pool = redis.ConnectionPool(**self.config)
        self.rds = redis.Redis(connection_pool=self.pool)
        self.pipe = self.rds.pipeline()
        self.support_type = ['string', 'hash', 'list', 'set', 'zset']

    def __str__(self):
        return 'Redis[{host}:{port}], db[{db}]'.format(**self.config)

    def exec(self):
        commands = self.kwargs.get('commands')
        result = []
        for command in commands:
            key_type = command.get('type')
            if key_type not in self.support_type:
                result.append(RuntimeError(f'Not support type, choice in [{self.support_type}]').__repr__())
                continue
            func_name = command.get('operate')
            key_name = command.get('name')
            args = command.get('args')
            kwargs = command.get('kwargs')

            rds_command = 'self.rds.%s("%s",' % (func_name, key_name)
            if args:
                rds_command += '*args,'
            if kwargs:
                rds_command += '**kwargs,'
            rds_command += ')'
            try:
                logger.info(f'RedisHandler exec command:{rds_command}.')
                result.append(eval(rds_command))
            except Exception as e:
                logger.error(f'exec{rds_command} redis throw exception[{e}]')
                logger.error(f'traceback.format_exc():\n{traceback.format_exc()}')
                result.append(e.__repr__())
        return result


if __name__ == '__main__':
    config = {
        'host': 'r-d9jabfe0f2736274.redis.ap-southeast-5.rds.aliyuncs.com',
        'port': 6379,
        'password': '1qaz@WSX',
        'db': 3,
        'commands': [
            {'type': 'string', 'operate': 'set', 'name': 'jackie', 'kwargs': {'value': 'abc'}},
            {'type': 'string', 'operate': 'get', 'name': 'jackie', },
            {'type': 'hash', 'operate': 'hset', 'name': 'jackie_hash', 'kwargs': {'key': 'kkk', 'value': 'vvv'}},
            {'type': 'list', 'operate': 'lpush', 'name': 'jackie_list', 'args': [1, 2, 3]},
            {'type': 'set', 'operate': 'sadd', 'name': 'jackie_set', 'args': [1, 2, 3]},
            {'type': 'zset', 'operate': 'zadd', 'name': 'jackie_zset', 'kwargs': {'mapping': {'a': 1, 'b': 2, 'c': 3}}},
            {'type': 'string', 'operate': 'get', 'name_test': 'jackie'},
            {'type': 'string', 'operate': 'get_test', 'name': 'jackie'},
            {'type': 'string_test', 'operate': 'get_test', 'name': 'jackie'},
        ],
    }
    rds = RedisHandler(**config)
    print(rds.exec())


def get_rds_handler(tag=None):
    return HandlerRedis(tag)
