# -*- coding: UTF-8 -*-
# @Time     : 2/3/21 8:24 PM
# @Author   : Jackie
# @File     : utilSftp.py

import paramiko
import os


class SshConnectError(Exception):
    pass


class UtilSftp:
    def __init__(self, config):  # 本地密钥文件路径
        self.host = config['host']
        if config['key_file']:
            self.pkey = paramiko.RSAKey.from_private_key_file(config['key_file'])
        else:
            self.pkey = config['key_file']
        self.ssh = self.__ssh_conn(self.host, config['username'], config['password'], self.pkey, int(config['port']))
        self.sftp = self.__sftp_conn()

    def close(self):
        if hasattr(self.ssh, "close"):
            self.ssh.close()

    def __ssh_conn(self, host, username, password, pkey, port):
        ssh = paramiko.SSHClient()  # 创建一个SSH客户端client对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.pkey:
                ssh.connect(hostname=host, port=int(port), username=username, pkey=pkey)  # 免密登陆方式
            else:
                ssh.connect(hostname=host, port=int(port), username=username, password=password)  # 密码认证
        except:
            raise SshConnectError("SSH Connect %s Error!" % host)
        else:
            return ssh

    # 返回sftp通道实例对象 方法
    def __sftp_conn(self):
        transport = self.ssh.get_transport()  # 1.先ssh连上，2.再建立通道
        sftp = paramiko.SFTPClient.from_transport(transport)  # 创建一个已连通的SFTP客户端通道。
        return sftp

    # 执行命令方法
    def exe_command(self, cmd, timeout=300):
        _, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)
        try:
            channel = stdout.channel
            # print('channel',channel)
            exit_code = channel.recv_exit_status()
            # print('exit_code',exit_code)报错返回码是127，没有报错是0
            stdout = stdout.read().strip()
            stderr = stderr.read().strip()
            return {"status": 1, "stdout": stdout, "stderr": stderr, 'exit_code': exit_code}
        except:
            return {"status": 0, "stdout": stdout, "stderr": stderr, 'exit_code': 127}

    # 文件上传下载方法
    def trans_file(self, local_path, remote_path, action, **kwargs):
        try:
            if action == 'push':
                dirname = os.path.dirname(remote_path)
                self.exe_command("mkdir -p %s" % dirname)
                self.sftp.put(local_path, remote_path)
                return {"status": 1, "message": 'sftp %s %s success!' % (self.host, action)}
            elif action == "pull":
                dirname = os.path.dirname(local_path)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                # if os.path.exists(local_path):
                #     os.remove(local_path)
                self.sftp.get(remote_path, local_path)
                return {"status": 1, "stdout": 'sftp %s %s success!' % (self.host, action), "stderr": ""}
        except Exception as e:
            return {"status": 0, "stderr": 'sftp %s %s failed %s' % (self.host, action, str(e)), "stdout": ""}

    @staticmethod
    def iter_local_path(abs_path):
        """遍历本机该目录中所以的文件，并返回"""
        result = set([])
        for j in os.walk(abs_path):
            print(j)
            base_path = j[0]
            file_list = j[2]
            for k in file_list:
                p = os.path.join(base_path, k)
                result.add(p)
        return result

    def iter_remote_path(self, abs_path):
        """获取远程主机abs_path下的所以文件"""
        result = set([])
        try:
            stat = str(self.sftp.lstat(abs_path))
            print('stat', stat)
        except FileNotFoundError:
            return result
        else:
            if stat.startswith("d"):
                file_list = self.exe_command("ls %s" % abs_path)["stdout"].decode(encoding='utf-8').strip().splitlines()
                # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。 Python splitlines(
                # ) 按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表，如果参数 keepends 为(默认值) False，不包含换行符，如果为 True，则保留换行符。

                for j in file_list:
                    p = os.path.join(abs_path, j)
                    result.update(self.iter_remote_path(p))  # 合并 并集U
            else:
                result.add(abs_path)
        return result
