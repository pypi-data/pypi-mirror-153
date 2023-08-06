#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests
import showlog
import json
import envx
from urllib.parse import urlparse

"""
企业微信文档：
    https://work.weixin.qq.com/api/doc/90000/90136/91770
    https://work.weixin.qq.com/help?person_id=1&doc_id=13376
    获取会话内容：https://work.weixin.qq.com/api/doc/90000/90135/91774
"""

env_file_name_default = 'webhook.env'
test_msg = 'This is a test message from lazywebhook. \nIf you see this message, the test was successful.'


def make_con_info(
        env_file_name: str = env_file_name_default
):
    # ---------------- 固定设置 ----------------
    inner_env = envx.read(file_name=env_file_name)
    if inner_env is None:
        return
    else:
        webhook = inner_env.get('webhook')
        if webhook is None:
            showlog.warning(f'环境文件[{env_file_name}]未设置webhook参数')
            return
        else:
            at_ids = inner_env.get('at_ids')
            if at_ids is not None:
                at_ids = at_ids.split(',')
            at_mobiles = inner_env.get('at_mobiles')
            if at_mobiles is not None:
                at_mobiles = at_mobiles.split(',')
            con_info = {
                "webhook": inner_env.get('webhook'),
                "at_ids": at_ids,  # 艾特的id，以英文逗号分隔
                "at_mobiles": at_mobiles  # 艾特的手机号码，以英文逗号分隔
            }
            return con_info
    # ---------------- 固定设置 ----------------


class WeixinBasics:
    def __init__(
            self,
            con_info: dict = None,
            webhook: str = None,
            at_ids: list = None,
            at_mobiles: list = None,
            is_at: bool = None,
            at_all: bool = None
    ):
        """
        初始化参数
        :param con_info: 参数字典，将每个参数以key-value形式存放在一起
        :param webhook: webhook地址
        :param at_ids: 按照id艾特的id列表
        :param at_mobiles: 按照手机号码艾特的手机号码列表
        :param is_at: 是否艾特
        :param at_all: 是否艾特所有人

        con_info为参数集合，如果其他参数未指定，将从con_info中获取参数
        如果at_all为True，将艾特所有人，不会另外单独艾特单独的用户
        如果需要单独艾特某些id，需设置is_at=True，否则不会生效

        """
        if webhook is None and con_info is not None:
            self.webhook = con_info.get('webhook')
        else:
            self.webhook = webhook

        if at_ids is None and con_info is not None:
            self.at_ids = con_info.get('at_ids')
        else:
            self.at_ids = at_ids

        if at_mobiles is None and con_info is not None:
            self.at_mobiles = con_info.get('at_mobiles')
        else:
            self.at_mobiles = at_mobiles

        if is_at is None and con_info is not None:
            self.is_at = con_info.get('is_at', False)
        else:
            self.is_at = is_at

        if at_all is None and con_info is not None:
            self.at_all = con_info.get('at_all', False)
        else:
            self.at_all = at_all

    def send_text(
            self,
            msg: str = None,

            con_info: dict = None,
            webhook: str = None,
            at_ids: list = None,
            at_mobiles: list = None,
            is_at: bool = None,
            at_all: bool = None
    ):
        """
        发送文本消息

        :param msg: 发送的文本内容
        :param con_info: 参数字典，将每个参数以key-value形式存放在一起
        :param webhook: webhook地址
        :param at_ids: 按照id艾特的id列表
        :param at_mobiles: 按照手机号码艾特的手机号码列表
        :param is_at: 是否艾特
        :param at_all: 是否艾特所有人

        正常返回：
            {'errcode': 0, 'errmsg': 'ok'}
        异常返回：
            未指定发送内容
                {'errcode': 44004, 'errmsg': 'empty content, hint: [1653883914340381947793508], from ip: 121.227.209.88, more info at https://open.work.weixin.qq.com/devtool/query?e=44004'}
            接口调用超过限制
                {'errcode': 45009, 'errmsg': 'api freq out of limit, hint: [1653710540075724015410106], from ip: 121.227.209.88, more info at https://open.work.weixin.qq.com/devtool/query?e=45009'}
            机器人webhookurl不合法或者机器人已经被移除出群
                {'errcode': 93000, 'errmsg': 'invalid webhook url, hint: [1653710655173452988930371], from ip: 121.227.209.88, more info at https://open.work.weixin.qq.com/devtool/query?e=93000'}
        """
        if msg is None:
            msg = test_msg

        if webhook is None and con_info is not None:
            webhook = con_info.get('webhook')
        else:
            if webhook is None:
                webhook = self.webhook

        if at_ids is None and con_info is not None:
            at_ids = con_info.get('at_ids')
        else:
            if at_ids is None:
                at_ids = self.at_ids

        if at_mobiles is None and con_info is not None:
            at_mobiles = con_info.get('at_mobiles')
        else:
            if at_mobiles is None:
                at_mobiles = self.at_mobiles

        if is_at is None and con_info is not None:
            is_at = con_info.get('is_at', False)
        else:
            if is_at is None:
                is_at = self.is_at

        if at_all is None and con_info is not None:
            at_all = con_info.get('at_all', False)
        else:
            if at_all is None:
                at_all = self.at_all

        if at_all is True:
            at_ids = ["@all"]
            at_mobiles = ["@all"]

        text_dict = {
            'content': msg
        }
        if at_all is True:
            text_dict['mentioned_list'] = ["@all"]
        else:
            if at_ids is not None and is_at is True:
                text_dict['mentioned_list'] = at_ids
            if at_mobiles is not None and is_at is True:
                text_dict['mentioned_mobile_list'] = at_mobiles
        data = {
            "msgtype": "text",
            "text": text_dict
        }
        inner_data = json.dumps(data, ensure_ascii=False)
        byte_data = inner_data.encode('utf-8')
        response = lazyrequests.lazy_requests(
            method='POST',
            url=webhook,
            data=byte_data,
            return_json=True
        )
        return response


def send_text(
        msg: str = None,

        env_file_name: str = None,
        webhook: str = None,
        at_ids: list = None,
        at_mobiles: list = None,
        is_at: bool = None,
        at_all: bool = None
):
    """
    在内部实例化，
    首先使用自定义参数，其次使用env参数
    """
    if env_file_name is not None:
        env_con_info = make_con_info(env_file_name=env_file_name)
    else:
        env_con_info = make_con_info()

    if webhook is None and env_file_name is not None and env_con_info is None:
        showlog.warning('webhook不能为空')
        return {'errcode': -1, 'errmsg': 'webhook不能为空'}
    elif webhook is None and env_file_name is not None and env_con_info is not None:
        webhook = env_con_info.get('webhook')

    if at_ids is None and env_file_name is not None and env_con_info is not None:
        at_ids = env_con_info.get('at_ids')

    if at_mobiles is None and env_file_name is not None and env_con_info is not None:
        at_mobiles = env_con_info.get('at_mobiles')

    con_info = {
        'webhook': webhook,
        'at_ids': at_ids,
        'at_mobiles': at_mobiles
    }
    webhook_hostname = urlparse(webhook).hostname
    if webhook_hostname == 'qyapi.weixin.qq.com':
        webhook_basic = WeixinBasics(con_info=con_info)
        response = webhook_basic.send_text(
            msg=msg,
            con_info=con_info,
            at_ids=at_ids,
            at_mobiles=at_mobiles,
            is_at=is_at,
            at_all=at_all
        )
        return response
    else:
        return {'errcode': -2, 'errmsg': '暂不支持此webhook'}
