#!/usr/bin/env python
# coding=utf-8

"""
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-03-22 12:57:35
LastEditors: zmf96
LastEditTime: 2022-03-24 15:19:49
FilePath: /cp-common/cp_common/utils.py
Description: 
"""

import base64
import inspect
from typing import List, Set, Tuple

from cp_common.log import logger


def parse_host(host: str) -> List[str]:
    return host.split(",")


def parse_port(port: str) -> List[str]:
    # TODO:解析 eg:1-65535
    port_list = port.split(",")
    port_list = list(set(port_list))
    port_list.remove("")
    return port_list


def get_url_list_from_host_port_list(
    host_list: List[str], port_list: List[str] = []
) -> Set[str]:
    url_list = set()
    for host in host_list:
        if port_list != [] and port_list != [""]:
            for port in port_list:
                if "443" in port:
                    url_list.add("https://" + host + ":" + port)
                else:
                    url_list.add("http://" + host + ":" + port)
        else:
            url_list.add("https://" + host)
            url_list.add("http://" + host)

    return url_list


def is_async_func(func_name) -> bool:
    return inspect.iscoroutinefunction(func_name)


def get_host_port_from_url(url: str) -> (str, str):
    host = ""
    port = "80"
    if "https" in url:
        port = "443"
    if "://" in url:
        url = url.split("://")[1]
    try:
        host = url.split(":")[0]
        if "/" in host:
            host = host.split("/")[0]
        port = url.split(":")[1]
        if "/" in port:
            port = port.split("/")[0]
    except Exception:
        pass
    return host, port


def get_basic_auth_str(username, password):
    temp_str = username + ":" + password
    # 转成bytes string
    bytesString = temp_str.encode(encoding="utf-8")
    # base64 编码
    encodestr = base64.b64encode(bytesString)
    return "Basic " + encodestr.decode()
