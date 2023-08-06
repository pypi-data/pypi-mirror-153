# -*- coding: UTF-8 -*-

from netmiko import ConnectHandler
from collections import namedtuple

class hillstone(object):
    def __init__(self,ac_info,dev_info):
        self.username = ac_info.username
        self.password = ac_info.password
        self.enable_pass = ac_info.enable_pass

        self.dev_name = dev_info.dev_name
        self.ip = dev_info.dev_ip
        self.dev_info = {
            'device_type': 'autodetect',
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
            'port': 22,
            'secret': self.enable_pass,
            'timeout': 3600,
            'verbose': True,
        }

    def account_verification(self, config_mode_tag="config"):
        """
        验证账号是否有配置权限，返回提示符
        :param
        :return: string
        """
        net_connect = ConnectHandler(**self.dev_info)
        net_connect.find_prompt()                  # 这句看似没用，但是如果没有，就会报错
        net_connect.write_channel("configure\n")
        net_connect.find_prompt()                  # 这句看似没用，但是如果没有，就会报错
        if config_mode_tag in net_connect.find_prompt():
            net_connect.disconnect()
            return True
        else:
            net_connect.disconnect()
            return False


    def get_running_config(self, filter_str = 'NULL', show_config_cmd='show configuration'):
        """
        获取设备配置信息，如果添加 running_content 参数，可以获取指定的配置信息
        返回的是一个字符串，这个字符串就是设备配置，或者指定的配置
        :selected param running_content = 'Key'
        :return: string
        """
        net_connect = ConnectHandler(**self.dev_info)
        net_connect.send_command("terminal length 0")
        if filter_str == 'NULL':
            running_config = net_connect.send_command(show_config_cmd)
        else:
            running_config = net_connect.send_command("{} | in {}".format(show_config_cmd, filter_str))
        net_connect.disconnect()
        return running_config


    def inspect_config(self, check_list):
        """
        该函数可以检查配置，check_list是一个字符串列表，可以按次序检查设备中是否有该配置的存在
        返回保存了检查结果的字符串
        :param check_list
        :return: string
        """
        net_connect = ConnectHandler(**self.dev_info)
        net_connect.send_command("terminal length 0")
        check_result = ""
        for line in check_list:
            show_configs = net_connect.send_command("show configuration | in " + line)
            check_result = check_result + show_configs + "\n"
        net_connect.disconnect()
        return check_result


    def inspect_session(self, check_list):
        """
        该函数可以检查防火墙的session，check_list是一个ip列表，可以检查该ip相关的session
        返回保存了检查结果的字符串
        :param 
        :return: True or False
        """
        if isinstance(check_list,str) : check_list = check_list.split("\n")

        net_connect = ConnectHandler(**self.dev_info)
        net_connect.send_command("terminal length 0")
        check_result = ""
        for line in check_list:
            show_configs = net_connect.send_command('show session src-ip ' + line)
            check_result = check_result + show_configs + "\n"
        net_connect.disconnect()
        return check_result


    def generate_routing_script(self,route_list):
        """
        生成路由的脚本，传入的参数是一个ip列表，如： [ "1.1.1.1","2.2.2.2" ]
        返回的是一个列表，这个列表的每一行，对应的脚本的每一行
        :param route_list: ["xxx","xxx"]
        :return: list
        """
        routing_script_list = []
        routing_script_list.append('ip vrouter "trust-vr"')
        for route_ip in route_list:
            routing_script_list.append('  ip route ' + route_ip.ip + ' ' + route_ip.next_hop)
        routing_script_list.append('exit')
        return routing_script_list


    def execute_script(self,access_script_list):
        """
        根据脚本实施命令，传入的参数是一个列表，如： [ "ip vrouter 'trust-vr'","  snatrule inxxxx", "exit" ]
        返回的是一个列表，这个列表的每一行，对应的命令的每一行
        :param route_list: ["xxx","xxx"]
        :return: list
        """
        if access_script_list == [] :
            return False

        net_connect = ConnectHandler(**self.dev_info)
        net_connect.send_command("terminal length 0")
        net_connect.write_channel("configure\n")

        for access_cmd_line in access_script_list:
            net_connect.write_channel(access_cmd_line + '\n')
        net_connect.write_channel("save\n")
        net_connect.write_channel("y")
        net_connect.write_channel("y")
        import time
        time.sleep(4)
        net_connect.disconnect()
        return True