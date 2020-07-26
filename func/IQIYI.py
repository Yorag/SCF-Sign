# -*- coding: utf8 -*-
import requests


class IQY:
    '''
    爱奇艺签到、抽奖
    *奖励：签7天奖1天，14天奖2天，28天奖7天；日常任务；随机成长值
    '''
    def __init__(self, P00001):
        '''
        :param P00001: cookies中必要参数
        '''
        self.P00001 = P00001
        self.taskList = []
        self.growthTask = 0


    def sign(self):
        '''
        签到
        '''
        url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
        params = {
             "P00001": self.P00001,
             "autoSign": "yes"
        }
        res = requests.get(url, params=params)
        if res.json()["code"] == "A00000":
            growth = res.json()["data"]["signInfo"]["data"]["rewardMap"]["growth"]
            continueSignDaysSum = res.json()["data"]["signInfo"]["data"]["continueSignDaysSum"]
            vipStatus = res.json()["data"]["userInfo"]["vipStatus"]
            rewardDay = 7 if continueSignDaysSum<=7 else (14 if continueSignDaysSum<=14 else 28)
            msg = f"VIP等级：{vipStatus}\n签到：+{growth}成长值\n已签到：{continueSignDaysSum}天/{rewardDay}天"
        else:
            print("（iqy）签到错误", res.content.decode())
            msg = f'错误代码：{res.json()["code"]}\n信息：{res.json()["msg"]}'
        return msg


    def draw(self):
        '''
        抽奖
        '''
        qyid = "f185cea041dfcbec15c66b7155041ba91100"
        psp_cki = "3a8I8x8XhLXRNA916m1SAJLBh2MJam2hz8Akg1i2GQ3KdPnpf5gYOOm2EXCm2u3QPwT4WLbf"

        url = "https://cards.iqiyi.com/views_category/3.0/vip_home"
        params1 = {
            "page_st": "suggest",
            "layout_v": 69.106,
            "app_k": "3179f25bc69e815ad828327ccf10c539",
            "dev_os": "5.1.1",
            "secure_p": "GPhone",
            "secure_v": 1,
            "psp_status": 3,
            "net_sts": 1,
            "lang": "zh_CN",
            "qyid": qyid,
            "app_v": "11.6.5",
            "dev_ua": "TAS-AN00",
            "platform_id": 10,
            "req_sn": 1594637758659
        }
        headers = {
            "t": "490079643",
            "sign": "087cfe72a655408f11a9083de5d869bb"
        }
        res = requests.get(url, params=params1, headers=headers)
        # 提取抽奖url前缀
        for i, card in enumerate(res.json()["cards"]):
            for j, block in enumerate(card["blocks"]):
                url = block.get("actions", {}).get("click_event", {}).get("data", {}).get("url")
                if url and url.startswith("http://iface2.iqiyi.com/"):
                    # 抽奖
                    params2 = {
                        "app_k": "3179f25bc69e815ad828327ccf10c549",
                        "app_v": "11.6.5",
                        "platform_id": 10,
                        "dev_os": "5.1.1",
                        "dev_ua": "TAS-AN00",
                        "net_sts": 1,
                        "qyid": qyid,
                        "psp_uid": 1626879399,
                        "psp_cki": psp_cki,
                        "psp_status": 3,
                        "secure_v": 1,
                        "secure_p": "GPhone",
                        "req_sn": 1594640282763
                    }
                    res = requests.get(url, params=dict(params1, **params2))
                    break
        print("（iqy）抽奖信息", res.json())
        if not res.json().get('code'):
            msg = res.json()["awardName"]
            return {"status": True, "msg": msg}
        else:
            try:
                msg = res.json()["kv"]["msg"]
            except:
                msg = res.json()["errorReason"]
            return {"status": False, "msg": msg}


    def queryTask(self):
        '''
        获取日常任务 和 taskCode
        '''
        url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
        params = {
            "P00001": self.P00001
        }
        res = requests.get(url, params=params)
        if res.json()["code"] == "A00000":
            for item in res.json()["data"]["tasks"]["daily"]:
                self.taskList.append({
                    "name": item["name"],
                    "taskCode": item["taskCode"],
                    "status": item["status"],
                    "taskReward": item["taskReward"]["task_reward_growth"]
                    })
        else:
            print("（iqy）获取任务失败")
        return self


    def joinTask(self):
        """
        遍历完成任务
        """
        url = "https://tc.vip.iqiyi.com/taskCenter/task/joinTask"
        params = {
            "P00001": self.P00001,
            "taskCode": "",
            "platform": "bb136ff4276771f3",
            "lang": "zh_CN"
        }
        # 遍历任务，仅做一次
        for item in self.taskList:
            if item["status"] == 2:
                params["taskCode"] = item["taskCode"]
                res = requests.get(url, params=params)


    def getReward(self):
        """
        获取任务奖励
        :return: 返回信息
        """
        url = "https://tc.vip.iqiyi.com/taskCenter/task/getTaskRewards"
        params = {
            "P00001": self.P00001,
            "taskCode": "",
            "platform": "bb136ff4276771f3",
            "lang": "zh_CN"
        }
        # 遍历任务，领取奖励
        for item in self.taskList:
            if item["status"] == 0:
                params["taskCode"] = item["taskCode"]
                res = requests.get(url, params=params)
                if res.json()["code"] == "A00000":
                    self.growthTask += item["taskReward"]
        msg = f"+{self.growthTask}成长值"
        return msg




if __name__ == '__main__':
    P00001 = ""
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
    print("【爱奇艺签到】", msg)
