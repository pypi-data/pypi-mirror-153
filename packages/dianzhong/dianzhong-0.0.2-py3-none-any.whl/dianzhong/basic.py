#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import lazysdk
import time


class Basics:
    def __init__(
            self,
            username: str = None,
            password: str = None,
            key: str = None
    ):
        self.username = username
        self.password = password
        self.key = key

    def get_token(
            self
    ):
        """
        获得token

        正确返回：
            {
                "code": 200,
                "message": "success",
                "data": {
                    "token": "*********************",
                    "expireSecond": 72244
                }
            }
        """
        url = f'http://provider.wuread.cn/auth/token?userName={self.username}&password={self.password}'
        return lazysdk.lazyrequests.lazy_requests(
            method='GET',
            url=url,
            return_json=True
        )

    def get_order_history(
            self,
            ctime_start: str = None,  # 2022-06-01 00:00:00
            ctime_end: str = None,  # 2022-06-01 23:59:59
            utime_start: str = None,  # 2022-06-01 00:00:00
            utime_end: str = None,  # 2022-06-01 23:59:59

            order_by: str = None,
            page: int = None,
            sort: str = None  # desc | asc
    ):
        """
        获取T+1订单数据

        :param ctime_start: 下单时间 开始时间，例如：2022-06-01 00:00:00
        :param ctime_end: 下单时间 结束时间，例如：2022-06-01 23:59:59
        :param utime_start: 订单更新时间 开始时间，例如：2022-06-01 00:00:00
        :param utime_end: token 订单更新时间 结束时间，例如：2022-06-01 23:59:59
        :param order_by: 排序字段
        :param page: 页码，0/1均为第1页，不填默认为第1页
        :param sort: 排序规则：desc | asc

        错误返回：传入数据为json才对
            {
                "timestamp": "2022-06-01T03:26:25.634+00:00",
                "status": 415,
                "error": "Unsupported Media Type",
                "message": "",
                "path": "/v4/query/result/452"
            }
        正确返回：
            {
                "code": 200,
                "message": "success",
                "data": {
                    "pageNum": 1,
                    "pageSize": 20,
                    "totalSize": 2,
                    "totalPage": 1,
                    "list": [
                        {
                            "channel_name": "第一章 摄政王",
                            "first_recharge": 0,
                            "utime": "2022-05-30 12:04:15",
                            "discount": 50.00,
                            "pay_channel_code": 2,
                            "optimizer_id": "4822",
                            "channel_code": "**********",
                            "book_id": "11010110171",
                            "type": 1,
                            "book_name": "权宠卦妃：摄政王的心上娇",
                            "optimizer_nickname": "**********",
                            "user_id": "**********",
                            "status_notify": 1,
                            "ctime": "2022-05-30 12:04:03",
                            "media_name": "头条",
                            "order_id": "**********",
                            "triggertime": "2022-05-27 20:44:21",
                            ...
                        },
                        {...}
                    ]
                }
            }
        """
        get_token_res = self.get_token()
        token = get_token_res['data']['token']
        item_id = '452'  # 看起来是固定的
        url = f'http://provider.wuread.cn/v4/query/result/{item_id}'
        headers = {
            'Authorization': token
        }
        filters = list()
        if ctime_start is not None:
            filters.append(f'ctime|>=|{ctime_start}')
        if ctime_end is not None:
            filters.append(f'ctime|<=|{ctime_end}')
        if utime_start is not None:
            filters.append(f'utime|>=|{utime_start}')
        if utime_end is not None:
            filters.append(f'utime|<=|{utime_end}')
        data = {
            "columnNames": [
                "id",
                "order_id",  # 订单号
                "user_id",  # 用户ID
                "channel_code",  # 渠道号
                "channel_name",  # 渠道名称
                "discount",  # 充值金额
                "pay_channel_code",  # 支付渠道
                "status_notify",  # 订单状态
                "type",  # 订单类型
                "ctime",  # 下单时间
                "register_date",  # 用户注册时间
                "book_id",  # 书籍ID
                "book_name",  # 书籍名称
                "triggertime",  # 触发时间
                "utime",  # 订单更新时间
                "first_recharge",  # 是否首冲
                "optimizer_id",  # 优化师账号
                "optimizer_nickname",  # 优化师昵称
                "media_name",  # 媒体名称
                "user_ad_accid",  # 广告账户ID
                "user_ad_plan_id",  # 广告计划ID
            ],
            "filters": filters,
            "limit": 0
        }
        if order_by is not None:
            data['orderBy'] = order_by
        if page is not None:
            data['page'] = page
        if sort is not None:
            data['sort'] = sort
        return lazysdk.lazyrequests.lazy_requests(
            method='POST',
            url=url,
            headers=headers,
            json=data,
            return_json=True
        )

    def get_order_real_time(
            self,
            key: str = None,
            req_id: str = None
    ):
        """
        获取实时订单数据，接口限制频率两分钟内只能获取一次数据（分页查询整体定义为一次查询）

        :param key: 密钥
        :param req_id: 请求序列号，page>1时必传

        错误返回：
            {
                "data": "",
                "message": "请勿频繁请求接口！",
                "status": 40005,
                "timestamp": "1654055725926"
            }
        正确返回（无数据）：
            {
                "data": {
                    "orders": "",
                    "reqId": ""
                },
                "message": "success",
                "status": 0,
                "timestamp": "1654055842684"
            }
        正确返回（有数据）：
            {
                'data': {
                    'orders': [
                        {
                            'bookId': '11010110171',
                            'bookName': '权宠卦妃：摄政王的心上娇',
                            'channelCode': '***********',
                            'channelCreateTime': '2022-05-2517: 32: 33',
                            'channelName': '颜清渊新第二章',
                            'ctime': '2022-05-3116: 20: 51',
                            'discount': 1.0,
                            'first_recharge': 1,
                            'id': '***********',
                            'media': '头条',
                            'optNickName': '***********',
                            'optUserName': '***********',
                            'payChannelCode': 1,
                            'regTime': '2022-05-2720: 43: 08',
                            'status': 1,
                            'triggerTime': '2022-05-2720: 43: 08',
                            'type': 1,
                            'userAdAccId': '***********',
                            'userAdPlanId': '***********',
                            'userId': '***********',
                            'utime': '2022-05-3116: 21: 17'
                        }
                    ],
                    'reqId': ''
                },
                'message': 'success',
                'status': 0,
                'timestamp': '1654069795964'
            }

        """
        url = f'http://xsmfcps.hzage.cn/glory-cps/order/dzafs'
        if key is None:
            key = self.key

        data = {
            "key": key,
            "startTime": lazysdk.lazytime.get_timestamp2datetime(int(time.time())-86400)
        }  # startTime：订单查询开始时间，结束时间为当前时间，最大时间跨度24小时
        if req_id is not None:
            data['reqId'] = req_id
        return lazysdk.lazyrequests.lazy_requests(
            method='POST',
            url=url,
            json=data,
            return_json=True
        )


def get_order_real_time(
        key: str = None,
        req_id: str = None
):
    """
    获取实时订单数据，接口限制频率两分钟内只能获取一次数据（分页查询整体定义为一次查询）

    :param key: 密钥
    :param req_id: 请求序列号，page>1时必传

    详细见class

    """
    url = f'http://xsmfcps.hzage.cn/glory-cps/order/dzafs'
    data = {
        "key": key,
        "startTime": lazysdk.lazytime.get_timestamp2datetime(int(time.time())-86400)
    }  # startTime：订单查询开始时间，结束时间为当前时间，最大时间跨度24小时
    if req_id is not None:
        data['reqId'] = req_id
    return lazysdk.lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json=data,
        return_json=True
    )
