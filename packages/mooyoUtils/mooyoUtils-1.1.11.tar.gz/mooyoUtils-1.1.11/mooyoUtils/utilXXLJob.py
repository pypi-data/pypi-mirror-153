# -*- coding: UTF-8 -*-
# @Time     : 9/18/21 4:00 PM
# @Author   : Jackie
# @File     : utilXXLJob.py

import datetime
import requests
import time

from .logger import logger
from .read_config import apollo_reader


class XXLJob:
    def __init__(self):
        self.base_url = apollo_reader.get_value('xxl.base.url')
        self.username = apollo_reader.get_value('xxl.username')
        self.password = apollo_reader.get_value('xxl.password')
        self.session = requests.session()

    # 登录
    def login(self, ):
        url = self.base_url + '/login'
        data = {'userName': self.username, 'password': self.password}
        response = self.session.post(url=url, data=data)
        if response.status_code == 200:
            logger.info(f'xxl user{self.username} login success.')
        else:
            logger.error(f'xxl user{self.username} login failed, response id [{response.text}]')

    # 获取job 列表
    def get_job_list(self, job_group, job_desc='', exe_handler=''):
        """

        :param job_group: 157: pipeline
        :param job_desc:
        :param exe_handler:
        :return:
        """
        url = self.base_url + '/jobinfo/pageList'
        data = {'jobGroup': job_group, 'jobDesc': job_desc, 'executorHandler': exe_handler, 'start': 0, 'length': 100}
        response = self.session.post(url=url, data=data)
        return response.json()

    # 获取job log 列表
    def get_job_log_list(self, job_group, job_id, status=-1, page_size=100):
        """

        :param job_group:
        :param job_id:
        :param status: -1: 进行中
        :param page_size:
        :return:
        """
        url = self.base_url + '/joblog/pageList'
        start_time = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y-%m-%d 00:00:00')
        end_time = (datetime.datetime.now() - datetime.timedelta(days=0)).strftime('%Y-%m-%d %H:%M:%S')
        filter_time = start_time + ' - ' + end_time
        params = {'jobGroup': job_group, 'jobId': job_id, 'logStatus': status, 'start': 0, 'length': page_size,
                  'filterTime': filter_time, '_': int(time.time()*1000)}
        response = self.session.get(url=url, params=params)
        logger.info('get job lost:job_group[%s], job_id[%s], start_time[%s], end_time[%s]'
                    % (job_group, job_id, start_time, end_time))
        return response.json()['data']

    # kill job log
    def kill_job_log(self, log_id):
        url = self.base_url + '/joblog/logKill'
        data = {'id': log_id}
        response = self.session.post(url=url, data=data)
        return response.json()

    # 执行job
    def run_job(self, job_id, executor_param=''):
        """

        :param executor_param: job 参数
        :param job_id:
        :return:
        """
        url = self.base_url + '/jobinfo/trigger'
        data = {'id': job_id, 'executorParam': executor_param}
        self.login()

        response = self.session.post(url=url, data=data)
        if response.status_code == 200:
            logger.info('run xxl job, job_id[%s] success' % job_id)
        else:
            logger.error(f'run xxl job, job_id[{job_id}] fail, response[{response.text}]')

    # 暂定job
    def pause_job(self, job_id):
        url = self.base_url + '/jobinfo/stop'
        data = {'id': job_id}

        self.session.post(url=url, data=data)
        logger.info('pause xxl jon, job_id[%s] success' % job_id)

    # 恢复job
    def resume_job(self, job_id):
        url = self.base_url + '/jobinfo/start'
        data = {'id': job_id}

        self.session.post(url=url, data=data)
        logger.info('resume xxl jon, job_id[%s] success' % job_id)
