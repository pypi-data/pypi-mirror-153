# -*- coding: UTF-8 -*-

from netmiko import ConnectHandler
from collections import namedtuple

class base_linux(object):
    def __init__(self,ac_info,dev_info):
        self.username = ac_info.username
        self.password = ac_info.password
        self.ip = dev_info.dev_ip

        self.conn_info = {
            'device_type': "linux",
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
            'port': 22,
            'timeout': 3600,
            'verbose': True,
        }


    def send_commands(self, commands = ""):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command(commands)
        net_connect.disconnect()
        return output


    def execute_script(self, commands = ""):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command(commands)
        net_connect.disconnect()
        return output


    # 查看一些信息
    def get_kernel_info(self):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command("cat /proc/version")
        net_connect.disconnect()
        return output


    def get_cup_info(self):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command("top -bn 1 -i -c")
        net_connect.disconnect()
        return output


    def get_mem_info(self):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command("cat /proc/meminfo")
        net_connect.disconnect()
        return output


    def get_running_config(self):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command("top -bn 1 -i -c")
        output = output + "\n" + net_connect.send_command("free")
        output = output + "\n" + net_connect.send_command("df -ha")
        output = output + "\n" + net_connect.send_command("ps -ef")
        net_connect.disconnect()
        return output


    # 系统操作，重启，关机
    def reboot(self):
        conn_info = self.conn_info
        net_connect = ConnectHandler(**conn_info)
        net_connect.write_channel("reboot")
        # ？这里都不需要在 reboot 后面加 \n ，就可以执行了
        # ？这里不可以使用 send_command, 会卡住
        net_connect.disconnect()


    def shutdown(self):
        conn_info = self.conn_info
        net_connect = ConnectHandler(**conn_info)
        net_connect.write_channel("shutdown now")
        net_connect.disconnect()


class redhat(base_linux):
    def get_sys_info(self):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command("cat /etc/redhat-release")
        net_connect.disconnect()
        return output


class centos(redhat):
    def get_sys_info(self):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command("cat /etc/redhat-release")
        net_connect.disconnect()
        return output


class ubuntu(base_linux):
    def get_sys_info(self):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command("lsb_release -a")
        net_connect.disconnect()
        return output


'''
class debian(base_linux):
    def get_sys_info(self):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command("cat /etc/redhat-release")
        net_connect.disconnect()
        return output

class suse(base_linux):
    def get_sys_info(self):
        net_connect = ConnectHandler(**self.conn_info)
        output = net_connect.send_command("cat /etc/redhat-release")
        net_connect.disconnect()
        return output
'''