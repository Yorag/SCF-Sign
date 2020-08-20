import re
import time
import requests


class TV:
    """
    腾讯视频签到
    *VIP签到两次
    """
    def __init__(self, cookies, params):
        '''
        初始化
        :param cookies: 
        :param params: 请求access.video.qq.com/user/auth_refresh?后的字符串
        '''
        self.params = params
        self.s = requests.session()
        # 设置cookies
        self.s.cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
        self.nickName = ""



    def auth_refresh(self):
        '''
        刷新信息
        '''
        url = "https://access.video.qq.com/user/auth_refresh"
        headers = {"referer": "https://v.qq.com/"}
        res = self.s.get(url, params=self.params, headers=headers)
        print("（tx）刷新信息", res.text)
        self.nickName = re.search('nick":"(.*?)"', res.content.decode()).group(1)



    def sign_once(self):
        '''
        一次签到
        '''
        url = "http://v.qq.com/x/bu/mobile_checkin"
        params = {
            "isDarkMode": 0,
            "uiType": "REGULAR"
        }
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 9 SE Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045230 Mobile Safari/537.36 QQLiveBrowser/8.2.35.21442"
        # }
        res = requests.get(url, params=params, cookies=self.s.cookies.get_dict())
        match = re.search(r'isMultiple" />\s+(.*?)\s+<', res.text)
        if match:
            value = match.group(1)
            msg = f"成长值{value}"
        elif res.content.decode() == "Unauthorized":
            msg = "身份过期"
        elif "签到失败" in res.content.decode():
            msg = "签到失败，检查参数设置"
        else:
            msg = "签到失败，自行登录网址签到http://v.qq.com/x/bu/mobile_checkin"
            print(res.request.headers)
            # print("（tx）一次签到", res.text)
        return msg



    def sign_twice(self):
        '''
        二次签到
        '''
        url = "https://vip.video.qq.com/fcgi-bin/comm_cgi"
        params = {
            "name": "hierarchical_task_system",
            "cmd": 2
        }
        res = self.s.get(url, params=params)
        ret = re.search('ret": (.*?),|}', res.text).group(1)
        if ret == "0":
            value = re.search('checkin_score": (.*?),', res.text).group(1)
            msg = f"成长值x{value}"
        else:
            msg = res.text
        print("（tx）二次签到", msg)
        return msg







if __name__ == '__main__':
    cookies = {
        'video_platform': "2",
        'vqq_access_token': '4C543E4B5BE7954C92FA6FC3588EBE82',
        'vqq_openid': 'E8B6F81FD949AF335BFA1657477B52DF',
        'main_login': 'qq',
        'vqq_vuserid': '719930041',
        'vqq_vusession': 'vlFyjjUZ5BwYEMQ9kqUM7w..'
        # 'vuserid': '719930041'
    }
    params = {
        'vappid': '11059694', 
        'vsecret': 'fdf61a6be0aad57132bc5cdf78ac30145b6cd2c1470b0cfe', 
        'type': 'qq', 
        'g_actk': '150450282'
    }
    obj = TV(cookies, params)
    obj.auth_refresh()
    msg = f"用户：{obj.nickName}\n签到(1)：{obj.sign_once()}\n签到(2)：{obj.sign_twice()}"
    print("【腾讯视频签到】", msg)