# -*- coding: UTF-8 -*-
# @Time     : 2/4/21 3:58 PM
# @Author   : Jackie
# @File     : utilFtp.py
import traceback
from ftplib import FTP_TLS
from .logger import logger


class UtilFtp:
    def __init__(self, config):
        self.config = config
        self.ftp = FTP_TLS(self.config['host'])
        if config['debug_level'] in ('0', '1', '2', 0, 1, 2):
            self.ftp.set_debuglevel(int(config['debug_level']))
        self.login()

    def login(self):
        logger.info('Start Login ftp[%s:%s]' % (self.config['host'], self.config['port']))
        self.ftp.auth()
        username, password = self.config['username'], self.config['password']
        self.ftp.login(user=username, passwd=password)
        self.ftp.makepasv()
        self.ftp.sendcmd('pbsz 0')
        self.ftp.set_pasv(True)
        self.ftp.prot_p()
        logger.info('Ftp Login success[%s]' % (self.config['username']))

    def upload(self, file_path, ftp_tar_path, **kwargs):
        logger.info('Start upload file[%s], tar[%s].' % (file_path, ftp_tar_path))
        with open(file_path, 'rb') as f_up:
            self.ftp.storbinary('STOR ' + ftp_tar_path, f_up, **kwargs)
        logger.info('Upload file[%s] success.' % ftp_tar_path)

    def download(self, ftp_file_path, tar_path, **kwargs):
        logger.info('Start download file[%s], tar[%s].' % (ftp_file_path, tar_path))
        with open(ftp_file_path, 'wb') as f_down:
            self.ftp.retrbinary('RETR %s' % tar_path, f_down.write, **kwargs)
        logger.info('Download file[%s] success.' % tar_path)

    def trans_file(self, source_path, tar_path, action, **kwargs):
        try:
            if action == 'push':
                self.upload(source_path, tar_path, **kwargs)
            elif action == 'pull':
                self.download(source_path, tar_path, **kwargs)
            else:
                logger.error('FTP un support action[%s].' % action)
                raise RuntimeError
        except Exception as e:
            logger.error('FTP [%s] file fail.Throw exception[%s]' % (action, str(e)))
            logger.error('traceback.format_exc():\n%s' % traceback.format_exc())

    def quit(self):
        self.ftp.quit()
        logger.info('Quit ftp success.')
