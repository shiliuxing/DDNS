#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
import os
import socket
try:
    # python2
    from urllib2 import urlopen
except ImportError:
    # python3
    from urllib.request import urlopen

DEBUG = False  # 是否打印错误

def default_v4():  # 默认连接外网的ipv4
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 53))
    ip = s.getsockname()[0]
    s.close()
    return ip


def default_v6():  # 默认连接外网的ipv6
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    s.connect(('8:8:8:8:8:8:8:8', 8))
    ip = s.getsockname()[0]
    s.close()
    return ip


def local_v6(i=0):  # 本地ipv6地址
    info = socket.getaddrinfo(socket.gethostname(), 0, socket.AF_INET6)
    if DEBUG:
        print(info)
    return info[int(i)][4][0]


def local_v4(i=0):  # 本地ipv4地址
    info = socket.getaddrinfo(socket.gethostname(), 0, socket.AF_INET)
    if DEBUG:
        print(info)
    return info[int(i)][-1][0]



def public_v4(url="http://v4.ipv6-test.com/api/myip.php"):  # 公网IPV4地址
    try:
        return urlopen(url, timeout=60).read()
    except Exception as e:
        if DEBUG:
            print(e)


def public_v6(url="http://v6.ipv6-test.com/api/myip.php"):  # 公网IPV6地址
    try:
        return urlopen(url, timeout=60).read()
    except Exception as e:
        if DEBUG:
            print(e)


def get_ip_config():
    if os.name == 'nt':  # windows:
        cmd = 'ipconfig'
    else:
        cmd = 'ifconfig'
    return os.popen(cmd).readlines()


def ip_regex_match(parrent_regex, match_regex):
    ip_pattern = re.compile(parrent_regex)
    matcher = re.compile(match_regex)
    for s in get_ip_config():
        addr = ip_pattern.search(s)
        if addr and matcher.match(addr.group(1)):
            return addr.group(1)


def regex_v4(reg): # ipv4 正则提取
    if os.name == 'nt':  # Windows: IPv4 xxx: 192.168.1.2
        regex_str = r'IPv4 .*: ([\d\.]*)?\W'
    elif os.uname()[0] == 'Darwin':  # MacOS: inet 127.0.0.1
        regex_str = r'inet ([\d\.]*)?\s'
    else:  # LINUX: inet addr:127.0.0.1
        regex_str = r'inet addr:([\d\.]*)?\s'
    return ip_regex_match(regex_str, reg)


def regex_v6(reg): # ipv6 正则提取
    if os.name == 'nt':  # Windows: IPv4 xxx: ::1
        regex_str = r'IPv6 .*: ([\:\dabcdef]*)?\W'
    elif os.uname()[0] == 'Darwin':  # MacOS: inet ::1
        regex_str = r'inet6 ([\:\dabcdef]*)?\s'
    else:  # LINUX: inet6 addr: ::1/128
        regex_str = r'inet6 addr: ([\:\dabcdef]*)/\d{1,3}\s'
    return ip_regex_match(regex_str, reg)

