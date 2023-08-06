# -*- coding: UTF-8 -*-


def ip_to_24(ip):
    """
    将一个ip地址转换成指定掩码 24 位置 的字符串
    :param ip = "171.19.0.222"
    :return: string
    """
    ip_m24 = ip.split(".")[0] + "." + ip.split(".")[1] + "." + ip.split(".")[2] + ".0"
    return ip_m24


def ip_to_28(ip):
    """
    将一个ip地址转换成指定掩码 28 位置 的字符串
    :param ip = "171.19.0.222"
    :return: string
    """
    ip_m28 = ip.split(".")[0] + "." + ip.split(".")[1] + "." + ip.split(".")[2] + "." + str(
        int(int(ip.split(".")[3]) // 16) * 16)
    return ip_m28


def ip_to_29(ip):
    """
    将一个ip地址转换成指定掩码 29 位置 的字符串
    :param ip = "171.19.0.222"
    :return: string
    """
    ip_m29 = ip.split(".")[0] + "." + ip.split(".")[1] + "." + ip.split(".")[2] + "." + str(
        int(int(ip.split(".")[3]) // 8) * 8)
    return ip_m29


def ip_to_30(ip):
    """
    将一个ip地址转换成指定掩码 30 位置 的字符串
    :param ip = "171.19.0.222"
    :return: string
    """
    ip_m30 = ip.split(".")[0] + "." + ip.split(".")[1] + "." + ip.split(".")[2] + "." + str(
        int(int(ip.split(".")[3]) // 4) * 4)
    return ip_m30


def ip_is_correct(ip):
    """
    判断一个字符串是否是一个ip地址
    :param ip = "184.4.0.0"
    :return: True or False
    """
    from re import compile
    p = compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False


def ip_is_valid(ip):
    return ip_is_correct(ip)