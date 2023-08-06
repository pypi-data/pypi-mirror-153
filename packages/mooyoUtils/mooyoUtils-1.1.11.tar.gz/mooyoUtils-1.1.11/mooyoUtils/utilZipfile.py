# -*- coding: UTF-8 -*-
# @Time     : 2/7/21 3:17 PM
# @Author   : Jackie
# @File     : utilZipfile.py

import zipfile
import os

from .logger import logger


class UtilZipfile:
    def __init__(self):
        self.util_zip = zipfile

    def zip_file(self, file_path):
        logger.info('Start zipfile[%s].' % file_path)
        filepath, file_name = os.path.split(file_path)
        zip_filename = file_name.split('.')[0]
        result_path = os.path.join(filepath, '{file_name}.zip'.format(file_name=zip_filename))
        zip_obj = self.util_zip.ZipFile(result_path, 'w', zipfile.ZIP_DEFLATED)
        zip_obj.write(file_path, arcname=file_name)
        zip_obj.close()
        logger.info('Zipfile success[%s], tar[%s]' % (file_path, result_path))
        os.remove(file_path)
        return result_path

    def zip_files(self, file_dir):
        if os.path.isdir(file_dir):
            files = os.listdir(file_dir)
            result_path = '{file_name}.zip'.format(file_name=file_dir)
            zip_obj = self.util_zip.ZipFile(result_path, 'w', zipfile.ZIP_DEFLATED)
            for file in files:
                filepath, file_name = os.path.split(file)
                zip_obj.write(filepath, arcname=file_name)
            zip_obj.close()
