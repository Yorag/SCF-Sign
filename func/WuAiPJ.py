# -*- coding: utf8 -*-
import re
import requests


class WuAiPJ:
    """
    吾爱破解论坛签到
    *签到得2个爱币
    """
    def __init__(self, cookies):
        """
        初始化设置参数
        :param cookies: 含必要参数的cookies
        """
        self.cookies = cookies


    def sign(self):
        '''
        签到
        '''
        url = "https://www.52pojie.cn/home.php"
        params = {
            "mod": "task",
            "do": "apply",
            "id": 2
        }
        res = requests.get(url, params=params, cookies=self.cookies)
        res.encoding = "gbk"
        if "任务已完成" in res.text:
            msg = '签到：+2吾爱币'
        elif "本期您已申请过此任务" in res.text:
            msg = '签到过了'
        elif "需要先登录" in res.text:
            msg = '未登录，请检查Cookies'
        else:
            print("（52）签到错误信息", res.text)
            msg = "未知错误，检查日志"
        return msg




if __name__ == '__main__':
    cookies = {
        "htVD_2132_saltkey": "",
        "htVD_2132_auth": ""
    }

    obj = WuAiPJ(cookies)
    msg = obj.sign()
    print("【吾爱论坛】", msg)
