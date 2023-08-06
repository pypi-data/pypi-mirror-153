# -*- coding: UTF-8 -*-

from netmiko import ConnectHandler
from collections import namedtuple

class juniper_junos(object):
    def __init__(self, ac_info, dev_info):
        self.username = ac_info.username
        self.password = ac_info.password
        self.enable_pass = ac_info.enable_pass

        self.dev_name = dev_info.dev_name
        self.ip = dev_info.dev_ip
        self.dev_info = {
            'device_type': "juniper_junos",
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
            'port': 22,
            'secret': self.enable_pass,
            'timeout': 3600,
            'verbose': True,
        }


    def account_verification(self, config_mode_tag="#"):
        """
        验证账号是否有配置权限，返回提示符
        :param
        :return: string
        """
        net_connect = ConnectHandler(**self.dev_info)
        net_connect.write_channel("configure\n")
        import time
        time.sleep(2)
        if config_mode_tag in net_connect.find_prompt():
            net_connect.disconnect()
            return True
        else:
            net_connect.disconnect()
            return False


    def get_running_config(self, filter_str = 'NULL', show_config_cmd='show configuration | display set'):
        """
        获取设备配置信息，如果添加 running_content 参数，可以获取指定的配置信息
        返回的是一个字符串，这个字符串就是设备配置，或者指定的配置
        :selected param running_content = 'Key'
        :return: string
        """
        net_connect = ConnectHandler(**self.dev_info)
        net_connect.send_command("set cli screen-length 0")
        if filter_str == 'NULL':
            running_config = net_connect.send_command(show_config_cmd)
        else:
            running_config = net_connect.send_command("{} | match {}".format(show_config_cmd, filter_str))
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
        net_connect.send_command("set cli screen-length 0")

        check_result = ""
        for line in check_list:
            show_configs = net_connect.send_command("show configuration | display set | match " + line)
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
        net_connect.send_command("set cli screen-length 0")

        check_result = ""
        for line in check_list:
            show_configs = net_connect.send_command("show security flow session source-prefix " + line)
            check_result = check_result + show_configs + "\n"

        for line in check_list:
            show_configs = net_connect.send_command("show security flow session destination-prefix " + line)
            check_result = check_result + show_configs + "\n"
        net_connect.disconnect()
        return check_result


    def execute_script(self, access_script_list):
        """
        根据脚本实施命令，传入的参数是一个列表，如： [ "ip vrouter 'trust-vr'","  snatrule inxxxx", "exit" ]
        返回的是一个列表，这个列表的每一行，对应的命令的每一行
        :param route_list: ["xxx","xxx"]
        :return: list
        """
        if access_script_list == [] :
            return False

        net_connect = ConnectHandler(**self.dev_info)
        # 第一步，实施脚本
        net_connect.send_config_set(access_script_list, exit_config_mode=False)
        net_connect.commit()
        net_connect.disconnect()
        return True


    def generate_routing_script(self, route_info_list):
        """
        生成路由的脚本，传入的参数是一个ip列表，如： [ "1.1.1.1","2.2.2.2" ]
        返回的是一个列表，这个列表的每一行，对应的脚本的每一行
        :param route_list: ["xxx","xxx"]
        :return: list
        """
        routing_script_list = []
        for route_item in route_info_list:
            routing_script_list.append('set routing-options static route ' + route_item.ip + '/24 next-hop ' + route_item.next_hop)
        return routing_script_list

    # def gen_routing_policy(self):
    pass