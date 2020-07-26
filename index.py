# -*- coding: utf8 -*-
import time
import json
import requests

from func.IQIYI import IQY
from func.TV import TV
from func.MGTV import MGTV
from func.WangYiYun import WangYiYun
from func.ECloud import ECloud
from func.WuAiPJ import WuAiPJ
from func.Ley import Ley
from func.BBS import JingYi


def sendMsg(key, content):
    '''
    通过Qmsg酱向QQ发送信息
    :param key: Qmsg酱密钥
    :param content: 发送内容
    '''
    url = f"https://qmsg.zendee.cn:443/send/{key}"
    params = {
        "msg": content
    }
    res = requests.get(url, params=params)
    print(res.json())


def iqy(P00001):
    '''爱奇艺引用'''
    # 签到
    obj = IQY(P00001)
    msg1 = obj.sign()
    # 抽奖
    msg2 = ""
    for i in range(3):
        ret = obj.draw()
        if ret["status"]:
            msg2 += ret["msg"] + ";"
    # 日常任务
    obj.queryTask().joinTask()
    msg3 = obj.queryTask().getReward()

    msg = f"{msg1}\n抽奖：{msg2}\n任务：{msg3}"
    return msg


def tv(cookies, params):
    '''腾讯视频引用'''
    obj = TV(cookies, params)
    obj.auth_refresh()
    msg = f"用户：{obj.nickName}\n签到(1)：{obj.sign_once()}\n签到(2)：{obj.sign_twice()}"
    return msg


def mg(params):
    '''芒果tv引用'''
    obj = MGTV(params)
    msg = obj.sign()
    return msg


def wyy(uin, pwd):
    '''网易云音乐引用'''
    obj = WangYiYun()
    if obj.login(uin, pwd):
        msg = f'用户：{obj.nickname}\n签到(1)：{obj.sign(0)}\n签到(2)：{obj.sign(0)}\n打卡：{obj.clock()}'
    else:
        msg = "登录失败，密码错误"
    return msg


def ecloud(user, pwd):
    '''天翼云盘引用'''
    obj = ECloud(user, pwd)
    msg = obj.main()
    return msg

def pj(cookies):
    '''吾爱破解论坛引用'''
    obj = WuAiPJ(cookies)
    msg = obj.sign()
    return msg

def ly(cookies):
    '''乐易论坛引用'''
    obj = Ley(cookies)
    msg = obj.sign()
    return msg


def jy(cookies):
    '''精易论坛引用'''
    obj = JingYi(cookies)
    msg = obj.sign()
    return msg




def main_handler(event, context):
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    key = data["SKey"]
    # 爱奇艺
    msg_iqy = ""
    for d in data["IQIYI"]:
        msg_iqy += iqy(d["P00001"])

    # 腾讯视频
    msg_tv = ""
    for d in data["TV"]:
        params = dict([p.split("=") for p in d["params"].split("&")])
        cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
        msg_tv += tv(cookies, params)

    # 芒果tv
    msg_mg = ""
    for d in data["MGO"]:
        params = dict([p.split("=") for p in d["params"].split("&")])
        msg_mg += mg(params)

    # 天翼云盘
    msg_ec = ""
    for d in data["ECLOUD"]:
        msg_ec += ecloud(d["user"], d["pwd"])

    # 吾爱论坛
    msg_52 = ""
    for d in data["52PJ"]:
        cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
        msg_52 += pj(cookies)

    # 乐易论坛
    msg_ly = ""
    for d in data["LEY"]:
        cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
        msg_ly += ly(cookies)

    # 精易论坛
    msg_jy = ""
    for d in data["BBS"]:
        cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
        msg_jy += jy(cookies)

    # 网易云音乐
    msg_wyy = ""
    for d in data["WYY"]:
        msg_wyy += wyy(d["uin"], d["pwd"])

    # 发送信息
    msg = f"【爱奇艺】\n{msg_iqy}\n\
【腾讯视频】\n{msg_tv}\n\
【芒果tv】\n{msg_mg}\n\
【天翼云盘】\n{msg_ec}\n\
【吾爱破解】\n{msg_52}\n\
【乐易】\n{msg_ly}\n\
【精易】\n{msg_jy}\n\
【网易云】\n{msg_wyy}"
    sendMsg(key, msg)
    return msg
