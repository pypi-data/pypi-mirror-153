# -*- encoding=utf-8 -*-
import logging
import os
import time


# 定义日志输出
def init_log():
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    if not os.path.exists('./logs'):
        os.makedirs('./logs')

    fh = logging.FileHandler(time.strftime('./logs/%Y%m%d', time.localtime(time.time())) + '.log')
    fh.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] %(filename)s[line:%(lineno)d]: %(message)s"))

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] %(filename)s[line:%(lineno)d]: %(message)s"))

    log.addHandler(fh)
    log.addHandler(sh)

    return log


logger = init_log()
