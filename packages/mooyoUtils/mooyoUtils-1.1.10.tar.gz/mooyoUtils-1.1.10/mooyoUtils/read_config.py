# -*- coding: UTF-8 -*-
"""
Before use this model, you must config env params first in your localhost.
eg:
    ENV=FAT;IDC=DEFAULT;APOLLO_META=http://apollo-configfat.adakamiapi.id;APP_ID=3000010122
You need change these param's values if you need.
"""
import os
from .logger import logger
from .pyapollo import ApolloClient

proDir = os.path.split(os.path.realpath(__file__))[0]


class ApolloConfigReader:
    def __init__(self):

        env, idc = os.getenv('ENV'), os.getenv('IDC')
        url, app_id = os.getenv('APOLLO_META'), os.getenv('APP_ID')

        self.env = env and env.lower()
        idc = idc and idc.lower()
        cluster = idc

        logger.info(f'Start Up! ENV[{self.env}], IDC[{idc}], APOLLO_META[{url}], APOLLO_APP_ID[{app_id}]')
        self.global_params = {'env': self.env, 'base_path': proDir}

        if url and app_id and idc:
            self.apollo_client = ApolloClient(app_id=app_id, cluster=cluster, config_server_url=url)
            self.apollo_client.start()
        else:
            self.apollo_client = None

    def get_configurations(self):
        if not self.apollo_client:
            self.__init__()
        return self.apollo_client.get_configurations()

    def get_value(self, key):
        if not self.apollo_client:
            self.__init__()
        if key in self.global_params:
            return self.global_params.get(key)
        return self.apollo_client.get_value(key)

    def set_params(self, key, value):
        self.global_params[key] = value

    def is_allow_env(self, *args, **kwargs):
        if self.env in set(args):
            return True
        else:
            logger.info('Env[%s] is not allowed.' % self.env)


# 读取Apollo配置
apollo_reader = ApolloConfigReader()
