# -*- coding: utf8 -*-
import random
import json
import base64
import codecs
import hashlib

import requests
import execjs


# 读取JS加密文件
with open("AES.js", "r", encoding="UTF-8") as f:
    AES_js = execjs.compile(f.read())



def RSA_encrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'),
             16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)



def AES_encrypt(text, key, iv):
    '''
    JS运行AES加密
    CBC加密模式
    '''
    encrypt_text = AES_js.call('AES_Encrypt', text, key, iv)
    return encrypt_text


class WangYiYun():
    def __init__(self):
        self.g = '0CoJUm6Qyw8W8jud'         # buU9L(["爱心", "女孩", "惊恐", "大笑"])的值
        self.b = "010001"                   # buU9L(["流泪", "强"])的值
        # buU9L(Rg4k.md)的值
        self.c = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.iv = "0102030405060708"        # 偏移量
        a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.i = "".join([a[random.randint(0, 61)] for s in range(16)])  # 随机生成长度为16的字符串

        self.urls = {
            "LOGINBYPHONE": "https://music.163.com/weapi/login/cellphone",
            "LOGINBYEMAIL": "https://music.163.com/weapi/login",
            "SIGN": "https://music.163.com/weapi/point/dailyTask",
            "DAKA": "http://music.163.com/weapi/feedback/weblog",
            "DETAIL": "https://music.163.com/weapi/v1/user/detail/{}",
            "RECOMMEND": "https://music.163.com/weapi/v1/discovery/recommend/resource",
            "GETSONG": "https://music.163.com/weapi/v3/playlist/detail"
        }
        self.grade = [10, 40, 70, 130, 200, 400, 1000, 3000, 8000, 20000]
        self.s = requests.session()
        self.nickname = ""



    def _requests(self, url, data):
        """
        重写网络请求
        :param url: 请求地址
        :param params: POST data参数，明文
        :return: 返回Response对象
        """
        encText = str(data)
        data = {
            'params': AES_encrypt(AES_encrypt(encText, self.g, self.iv), self.i, self.iv),
            'encSecKey': RSA_encrypt(self.i, self.b, self.c)
        }
        res = self.s.post(url, data=data)
        return res


    def login(self, pwd, phone=None, email=None):
        """
        登录网易云，邮箱手机账号二选一
        :param pwd: 网易云密码
        :param email: 网易云邮箱账号
        :param phone: 网易云手机账号
        :return: 判断登录是否成功
        """
        if phone:
            url = self.urls["LOGINBYPHONE"]
            data = {
                "phone": phone,
                "countrycode": "86",
                "password": hashlib.md5(pwd.encode()).hexdigest(),
                "rememberLogin": "false"
            }
        else:
            url = self.urls["LOGINBYEMAIL"]
            data = {
                "username": email,
                "password": hashlib.md5(pwd.encode()).hexdigest(),
                "rememberLogin": "false"
            }
        res = self._requests(url, data=data)
        print("（wyy）登录", res.json())
        if res.json()["code"] == 200:
            self.nickname = res.json()["profile"]["nickname"]
            self.uid = res.json()["profile"]["userId"]
            return True
        else:
            return False



    def sign(self, type):
        """
        日常签到
        :param type: 签到，参数填0/1
        :return: 信息
        """
        data = {
            "type": type
        }
        res = self._requests(self.urls["SIGN"], data=data)
        print("（wyy）签到", res.json())
        if res.json()["code"] == 200:
            msg = f"+{res.json()['point']}经验"
        else:
            msg = res.json()["msg"]
        return msg


    def clock(self):
        """
        300首音乐打卡
        :return: 信息
        """
        playlist = self.recommend()
        songs = []
        flag = True
        # 填充songs信息列表
        while flag:
            playId = playlist[random.randint(0, len(playlist)-1)]
            songsId = self.getSongsId(playId)
            for id in songsId:
                songs.append({
                    "action": "play",
                    "json": {
                        "download": 0,
                        "end": "playend",
                        "id": id,
                        "sourceId": "",
                        "time": 240,
                        "type": "song",
                        "wifi": 0
                    }
                })
                if len(songs) >= 510:
                    flag = False
                    break
        data = {
            "logs": json.dumps(songs)
        }
        res = self._requests(self.urls["DAKA"], data=data)
        print("（wyy）歌单打卡", res.json())
        if res.json()["code"] == 200:
            msg = f"打卡{len(songs)}首歌"
        else:
            msg = res.json()["message"]
        return msg


    def detail(self):
        """
        查询个人信息
        """
        data = {}
        res = self._requests(self.urls["DETAIL"].format(self.uid), data=data)
        print("（wyy）详细信息", res.json())
        if res.json()["code"] == 200:
            for c in self.grade:
                if res.json()['listenSongs'] < c:
                    tip = f"还需听{c-res.json()['listenSongs']}首升级"
                    break
                else:
                    tip = "恭喜你已经满级了"
            msg = f"{res.json()['level']}级，{tip}"
        else:
            msg = res.json()["msg"]
        return msg



    def recommend(self):
        """
        获取歌单id列表
        :return: 返回歌单id列表
        """
        data = {
            "csrf_token": self.s.cookies.get_dict()["__csrf"]
        }
        res = self._requests(self.urls["RECOMMEND"], data)
        playlist = [i["id"] for i in res.json()["recommend"]]
        return playlist


    def getSongsId(self, playId):
        """
        获取歌曲id列表
        :param playId: 歌单id
        :return: 歌单所含歌曲id列表
        """
        data = {
            "id": playId,
            "n": 1000
        }
        res = self._requests(self.urls["GETSONG"], data)
        songsId = [i["id"] for i in res.json()["playlist"]["trackIds"]]
        return songsId







if __name__ == '__main__':
    email = ""
    phone = ""
    pwd = ""

    obj = WangYiYun()
    if obj.login(pwd, phone, email):
        msg = f'用户：{obj.nickname}\n签到(1)：{obj.sign(0)}\n签到(2)：{obj.sign(1)}\n打卡：{obj.clock()}\n信息：{obj.detail()}'
    else:
        msg = "登录失败，密码错误"
    print("【网易云签到】", msg)
