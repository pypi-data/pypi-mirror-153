# -*- coding: UTF-8 -*-
# @Time     : 2020/7/14 20:36
# @Author   : Jackie
# @File     : wechatRobot.py

import requests
from .logger import logger
from .read_config import apollo_reader


class WechatRobot:
    def __init__(self, *args, **kwargs):
        if not kwargs.get('robot_key'):
            self.robot_key = apollo_reader.get_value('weCom.robot.key')
            if not self.robot_key:
                self.robot_key = '4d52b92b-a125-48f1-8934-92c6cabf4a8d'
        else:
            self.robot_key = kwargs.get('robot_key')
        self.base_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook'
        self.message_url = self.base_url + '/send?key=%s' % self.robot_key
        self.upload_url = self.base_url + '/upload_media?key={robot_key}&type=file'.format(robot_key=self.robot_key)

    def send_message(self, message_body, msg_type='markdown'):
        msg = {
            'msgtype': msg_type,
            msg_type: message_body
        }
        response = requests.post(url=self.message_url, json=msg)
        if response.status_code == 200:
            logger.info('send weCom message success, message_body[%s]' % message_body)
            return {'result': 0}
        else:
            logger.error('send weCom message fail, message_body[%s], response[%s]' % (message_body, response.text))
            return {'result': -1}

    def get_media_id(self, file_path):
        file_name = file_path.split('/')[-1]
        files = [('file', (file_name, open(file_path, 'rb'), 'text/csv'))]
        payload = {'media': file_name, 'file': file_name, 'filename': file_name}
        headers = {'Content-Type': 'multipart/form-data'}
        response = requests.post(self.upload_url, headers=headers, data=payload, files=files)
        if response.status_code == 200:
            return response.json()['media_id']
        else:
            logger.error('WeCom get media id error, response[%s]' % response.text)
            raise RuntimeError

    def send_file(self, file_path):
        media_id = self.get_media_id(file_path)
        msg_data = {'media_id': media_id}
        self.send_message(msg_data, msg_type='file')
