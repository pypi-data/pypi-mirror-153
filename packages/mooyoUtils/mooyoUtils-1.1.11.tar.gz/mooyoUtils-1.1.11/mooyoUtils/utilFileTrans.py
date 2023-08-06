# -*- coding: UTF-8 -*-
# @Time     : 2/7/21 6:25 PM
# @Author   : Jackie
# @File     : utilFileTrans.py

from .logger import logger
from .utilFtp import UtilFtp
from .utilSftp import UtilSftp


class UtilFileTrans:
    def __init__(self, trans_type, config):
        """

        :param config: dict.
            if trans_type == ftp: need params[host, port, username, password, debug_level*]
            elif trans_type == sftp: need params[host, port, username, password, key_path*]
        """
        if trans_type not in ('ftp', 'sftp'):
            logger.error('Un support transfer type[%s].' % trans_type)
            raise RuntimeError
        if trans_type == 'ftp':
            self.util_file_transfer = UtilFtp(config)
        elif trans_type == 'sftp':
            self.util_file_transfer = UtilSftp(config)

    def trans_file(self, source_path, tar_path, action, **kwargs):
        self.util_file_transfer.trans_file(source_path, tar_path, action, **kwargs)


