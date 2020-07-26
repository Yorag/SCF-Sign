# -*- coding: utf8 -*-
import time
import json
import requests



class MGTV:
    '''
    芒果签到
    *奖励：连签21天，得15天体验会员；对应积分
    '''
    def __init__(self, params):
        '''
        初始化
        :param params: url关键字credits.bz.mgtv.com/user/creditsTake的?后所有参数
        '''
        self.params = params
        self.params["timestamp"] = round(time.time())


    def sign(self):
        '''
        签到
        :return: 返回信息
        '''
        url = "https://credits.bz.mgtv.com/user/creditsTake"
        res = requests.get(url, params=self.params)
        res_json = json.loads(res.content.decode().replace("__jp5(", "").replace(");", ""))
        print("（mgtv）签到信息", res.content.decode())
        if res_json["code"] == 200:
            curDay = res_json["data"]["curDay"]
            credits = res_json["data"]["credits"]
            msg = f"签到：+{credits}积分\n已签到：{curDay}天/21天"
        else:
            msg = "签到失败"
        return msg




if __name__ == '__main__':
    params = {
        "uuid": "bd86ab29595d4a0292068af3b0b35e8a",
        "ticket": "BS6L3HDQ6DI6LUD2PFF0",
        "type": 1
    }
    obj = MGTV(params)
    msg = obj.sign()
    print("【芒果tv签到】", msg)