# -*- coding: UTF-8 -*-
# @Time     : 5/21/21 4:57 PM
# @Author   : Jackie
# @File     : handlerEmail.py

from email.header import Header
from email.mime.text import MIMEText
import smtplib

from .logger import logger


def get_email_server(email_config):
    # email 相关配置
    from_addr = email_config['username']
    password_email = email_config['password']
    smtp_server = email_config['server.host']
    smtp_port = int(email_config['server.port'])
    email_timeout = email_config['timeout']

    if type(email_timeout) not in (int, float, str):
        email_timeout = 60
    else:
        email_timeout = float(email_timeout)

    server = smtplib.SMTP(smtp_server, smtp_port, timeout=email_timeout)
    # server.connect(host=smtp_server, port=smtp_port)
    server.starttls()
    server.login(from_addr, password_email)
    return server


class HandlerEmail:
    def __init__(self, email_config):
        self.email_config = email_config
        self.to_addr_list = email_config['receivers']
        self.subject = email_config['title']
        self.body = email_config['content']

    def send_email(self, subtype='html'):
        msg = MIMEText('%s' % self.body, _subtype=subtype, _charset='utf-8')

        msg['From'] = self.email_config['username']
        msg['To'] = ','.join(self.to_addr_list)
        msg['Subject'] = Header('%s' % self.subject, 'utf-8').encode()

        server = get_email_server(self.email_config)

        try:
            server.sendmail(self.email_config['username'], self.to_addr_list, msg.as_string())
            logger.info("send email success. to[%s], subject[%s]" % (str(self.to_addr_list), self.subject))
            return True
        finally:
            server.quit()
