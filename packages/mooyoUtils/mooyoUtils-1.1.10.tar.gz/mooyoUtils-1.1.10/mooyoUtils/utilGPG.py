# -*- coding: UTF-8 -*-
# @Time     : 2/3/21 8:24 PM
# @Author   : Jackie
# @File     : utilGPG.py

import os
import gnupg
from .logger import logger


class UtilGPG:
    def __init__(self, verbose=False):
        """
        GPG工具类
        :param verbose: 是否打印详情日志
        """
        self.gpg = gnupg.GPG(verbose=verbose)
        self.pub_key, self.fingerprint, self.recipients = None, None, None

    def create_cert(self, passphrase, name_real, name_email, key_type="RSA", key_length=1024):
        self.gpg.encoding = 'utf-8'
        input_data = self.gpg.gen_key_input(passphrase=passphrase, name_real=name_real, name_email=name_email,
                                            key_type=key_type, key_length=key_length)
        key = self.gpg.gen_key(input_data)
        logger.info('已生成key：{0}'.format(key))
        return key

    def export_cert(self, key, secret=False, passphrase=None):
        if secret:
            assert passphrase is not None, 'the param `passphrase` is required'
            logger.info(passphrase)
            ascii_armored_private_keys = self.gpg.export_keys(key, secret=True, passphrase=passphrase)
            with open('%s_private.asc' % key, mode='w') as f1:
                f1.write(ascii_armored_private_keys)
        else:
            ascii_armored_public_keys = self.gpg.export_keys(key)
            with open('%s_public.asc' % key, mode='w') as f1:
                f1.write(ascii_armored_public_keys)

    def get_cert(self, path):
        logger.info('Start get pub cert[%s].' % path)
        os.system('gpg --import %s' % path)
        with open(path, 'r') as f:
            pub_key = ascii(f.read())

        self.pub_key = self.gpg.import_keys(pub_key)
        self.fingerprint = self.gpg.list_keys()
        logger.info('Public cert fingerprint[%s], pub_key[%s].' % (str(self.fingerprint), self.pub_key.results))
        self.recipients = self.fingerprint[0]['uids'][0]

    def encrypt_file(self, file_path):
        logger.info('Start encrypt file[%s].' % file_path)
        stream = open(file_path, mode='rb')
        filepath, file_name = os.path.split(file_path)
        output_file_name = "{0}.gpg".format(file_name)
        output_file_path = os.path.join(filepath, output_file_name)
        self.gpg.encrypt_file(stream, always_trust=True, recipients=self.recipients, output=output_file_path, armor=False)
        logger.info('Encrypt file success[%s], result[%s].' % (output_file_path, output_file_path))
        return output_file_path

    def decrypted_file(self, file_path, out_file, private_cert_path, passphrase=None, ):
        # 导入私钥
        command = "gpg --import {0}".format(private_cert_path)
        print(command)
        os.system(command)
        filepath, file_name = os.path.split(file_path)
        stream = open(file_name, mode='rb')
        decrypted_data = self.gpg.decrypt_file(stream, passphrase=passphrase)
        print('解析成功')
        # 返回值为 gnupg.Crypt 类型。
        with open(out_file, 'w') as f:
            f.write(str(decrypted_data))
