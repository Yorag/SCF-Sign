# -*- coding: utf8 -*-
import re
import requests


class JingYi:
    """
    精易论坛签到
    """
    def __init__(self, cookies):
        """
        初始化参数
        :param cookies: 仅含关键参数即可
        """
        self.cookies = cookies
        self.url = "https://bbs.125.la/plugin.php"
        self.formhash = ""

        self.load()


    def _requests(self, method, params, data=None):
        '''
        重写requests请求
        :param method: 请求方法
        :param params: url表单值
        :param data: post请求数据
        :return: utf8编码后的response对象
        '''
        if method.upper() == "GET":
            res = requests.get(self.url, params=params, cookies=self.cookies)
        elif method.upper() == "POST":
            res = requests.post(self.url, params=params, data=data, cookies=self.cookies)
        res.encoding = "utf-8"
        return res


    def load(self):
        '''
        加载网页获取formhash值
        '''
        params = {"id": "dsu_paulsign:sign"}
        res = self._requests("GET", params=params)
        try:
            self.formhash = re.search("formhash=(.*?)&", res.text).group(1)
            print(f"{'-'*10}精易formhash值：{self.formhash}{'-'*10}")
        except:
            print("cookie过期")
            # print("res.content.decode()")
            pass


    def sign(self):
        '''
        签到
        '''
        params = {
            "id": "dsu_paulsign:sign",
            "operation": "qiandao",
            "infloat": 1
        }
        data = {
            "formhash": self.formhash,
            "submit": 1,
            "qdxq": "kx"
        }
        res = self._requests("POST", params=params, data=data)
        print(f"{'-'*10}精易签到json：{res.content.decode('gbk')}{'-'*10}")
        try:
            if res.json()["status"] == 1:
                # 签到成功
                content = f"签到：+{res.json()['data']['credit']}精币"
            elif res.json()["status"] == 0:
                # 已经签到过了
                content = res.json()["msg"]
            else:
                content = "cookies过期"
        except:
            content = "参数设置错误"
        return content





if __name__ == '__main__':
    cookies = {
        "lDlk_ecc9_saltkey": "",
        "lDlk_ecc9_auth": ""
    }

    obj = JingYi(cookies)
    if obj.formhash:
        msg = obj.sign()
    else:
        msg = "cookie过期"
    print("【精易论坛】", msg)

