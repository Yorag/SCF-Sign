# -*- coding: utf8 -*-
import time
import json
import requests



class MGTV:
    '''
    芒果签到
    *奖励：连签21天，得15天体验会员；对应积分
    '''
    def __init__(self, uuid, ticket):
        '''
        初始化
        :param uuid: uuid
        :param ticket: ticket
        '''
        self.uuid = uuid
        self.ticket = ticket
        self.urls = {
            "APP_SIGN": "https://credits.bz.mgtv.com/user/creditsTake",
            "PC_SIGN": "https://task.bz.mgtv.com/user/task_take",
            "WR_COMMENT": "https://task.bz.mgtv.com/credits/toast"
        }


    def sign_app(self):
        '''
        签到
        :return: 返回信息
        '''
        params = {
            "type": 1,
            "uuid": self.uuid,
            "ticket": self.ticket
        }
        res = requests.get(self.urls["APP_SIGN"], params=params)
        res_json = json.loads(res.content.decode().replace("__jp5(", "").replace(");", ""))
        print("（mgtv）签到信息(1)", res.content.decode())
        if res_json["code"] == 200:
            curDay = res_json["data"]["curDay"]
            credits = res_json["data"]["credits"]
            msg = f"+{credits}积分\n已签到：{curDay}天/21天"
        else:
            msg = "签到失败"
        return msg


if __name__ == '__main__':
    uuid = ""
    ticket = ""

    obj = MGTV(uuid, ticket)
    msg = f"签到：{obj.sign_app()}"
    print("【芒果TV】", msg)