#!/usr/bin/env python
# coding=utf-8

"""
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-03-22 14:12:49
LastEditors: zmf96
LastEditTime: 2022-03-24 14:12:22
FilePath: /cp-common/cp_common/base.py
Description:
"""

import datetime
import json
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed

from .log import logger
from .req import Requests

MAX_WORKERS = 50


class PortListField:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        self._validate_value(value)
        instance.__dict__[self._name] = value

    def _validate_value(self, value):
        if not isinstance(value, list):
            raise TypeError("Port must be an list")
        for v in value:
            if not isinstance(v, str):
                raise TypeError(
                    'Port must be an list[str], eg: ["80","443","8080-8090"]'
                )
            if v.isdigit() is False:
                self.__validate_value_int(v)
            else:
                self.__validate_value_range(v)

    def __validate_value_range(self, value):
        if "-" in value:
            start, end = value.split("-")
            if not start.isdigit() or not end.isdigit():
                raise TypeError(
                    'Port must be an list[str], eg: ["80","443","8080-8090"]'
                )
            if int(start) > int(end):
                raise TypeError(
                    'Port must be an list[str], eg: ["80","443","8080-8090"]'
                )

    def __validate_value_int(self, value):
        if not value.isdigit():
            raise TypeError('Port must be an list[str], eg: ["80","443","8080-8090"]')
        else:
            if int(value) < 0 or int(value) > 65535:
                raise TypeError("port must be in range 0-65535")


class Plugin(object):
    plugin_name = "Plugin"
    author = "Plugin"
    version = "0.1.4"
    base_dir = "./"
    logger = logger
    usage = [
        {
            "name": "host_list",
            "type": "List[str]",
            "usage": 'IP或域名列表，eg: ["127.0.0.1","localhost"]',
        },
        {
            "name": "port_list",
            "type": "List[str]",
            "usage": '端口列表，eg: ["80","443"]',
        },
        {
            "name": "keyword",
            "type": "str",
            "usage": '关键字, eg: "京ICP备12345678号"',
        },
        {
            "name": "domain_list",
            "type": "List[str]",
            "usage": '域名列表，eg: ["baidu.com","bing.com"]',
        },
        {
            "name": "url_list",
            "type": "List[str]",
            "usage": 'url列表，eg: ["http://baidu.com:80/","http://bing.com"]',
        },
        {"name": "args", "type": "**args", "usage": "func(**args))"},
    ]

    _thread_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        self.results = []

    @classmethod
    def verify_depend(cls) -> bool:
        """检查依赖是否就绪

        首次加载时，检查依赖是否就绪
        Returns:
            bool: True or False
        """
        return True

    @staticmethod
    def vaildator_kwargs(kwargs: dict) -> bool:
        """验证参数

        Raises:
            NotImplementedError: _description_

        Returns:
            bool: True or False
        """
        # TODO: 验证默认的三个参数
        return True

    def init(self):
        """不方便写在__init__()的初始化操作

        例如一些需要异步获取的参数，或者是为了与
        Raises:
            NotImplementedError: _description_
        """
        pass

    def save(self) -> None:
        """保存结果到json文件中"""
        path = (
            self.base_dir
            + self.plugin_name
            + "__"
            + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".json"
        )
        with open(path, "w") as f:
            json.dump(self.results, f)

    def close(self) -> None:
        """运行结束后，进行资源的清理工作

        Raises:
            NotImplementedError: _description_
        """
        pass

    @abstractmethod
    def run(self) -> None:
        """运行插件

        必须在子类中实现run方法
        """
        self.logger.info(self.kwargs)
