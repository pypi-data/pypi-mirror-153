# -*- coding: UTF-8 -*-
# @Time     : 2021/11/4 13:56
# @Author   : Jackie
# @File     : setup.py

# coding: utf-8

from setuptools import setup, find_packages
import sys
import os

if sys.version_info < (3, 5):
    sys.exit('Python 3.5 or greater is required.')


with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'README.md'), 'r') as fp:
    readme = fp.read()

VERSION = "1.1.11"

LICENSE = "MIT"

setup(
    name='mooyoUtils',
    version=VERSION,
    description='mooyo 常用工具包',
    long_description=readme,
    author='Jackie Chen',
    author_email='mooyo@live.cn',
    maintainer='Jackie Chen',
    maintainer_email='mooyo@live.cn',
    license=LICENSE,
    packages=find_packages(),
    platforms=["all"],
    url='http://git.ppdaicorp.com/chenqiang08/mooyoUtils.git',
    # INSTALL_REQUIRES 模块所依赖的python模块
    install_requires=['portion', 'demjson', 'python-dateutil', 'paramiko', 'redis', 'jsonpath', 'pymysql',
                      'apscheduler', 'requests', 'xlrd', 'pymongo', 'SQLAlchemy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries'
    ],
)
