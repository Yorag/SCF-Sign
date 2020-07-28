# -*- coding: utf8 -*-
import time
import requests


class IQY:
    '''
    爱奇艺签到、抽奖、做任务(签到、任务仅限VIP)
    *奖励：签7天奖1天，14天奖2天，28天奖7天；日常任务；随机成长值
    '''
    def __init__(self, P00001, psp_uid):
        '''
        :param P00001: 签到，任务，抽奖必要参数
        :param psp_uid: 抽奖必要参数
        '''
        self.P00001 = P00001
        self.psp_uid = psp_uid

        self.taskList = []
        self.growthTask = 0


    def sign(self):
        '''
        VIP签到
        '''
        url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
        params = {
             "P00001": self.P00001,
             "autoSign": "yes"
        }
        res = requests.get(url, params=params)
        print("（iqy）签到信息", res.json())
        if res.json()["code"] == "A00000":
            try:
                growth = res.json()["data"]["signInfo"]["data"]["rewardMap"]["growth"]
                continueSignDaysSum = res.json()["data"]["signInfo"]["data"]["continueSignDaysSum"]
                rewardDay = 7 if continueSignDaysSum<=7 else (14 if continueSignDaysSum<=14 else 28)
                msg = f"+{growth}成长值\n已签到：{continueSignDaysSum}天/{rewardDay}天"
            except:
                msg = res.json()["data"]["signInfo"]["msg"]
        else:
            print("（iqy）签到错误", res.content.decode())
            msg = f'错误代码：{res.json()["code"]}\n信息：{res.json()["msg"]}'
        return msg


    def queryTask(self):
        '''
        获取VIP日常任务 和 taskCode(任务状态)
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



    def draw(self, type):
        '''
        查询抽奖次数(必),抽奖
        :param type: 类型。0查询次数；1抽奖
        :return: {status, msg, chance}
        '''
        url = "https://iface2.iqiyi.com/aggregate/3.0/lottery_activity"
        params = {
            "lottery_chance": 1,
            "app_k": "3179f25bc69e815ad828327ccf10c539",
            "app_v": "11.6.5",
            "platform_id": 10,
            "dev_os": "5.1.1",
            "dev_ua": "TAS-AN00",
            "net_sts": 1,
            "qyid": "f185cea041dfcbec15c66b7155041ba91100",
            "psp_uid": self.psp_uid,
            "psp_cki": self.P00001,
            "psp_status": 3,
            "secure_v": 1,
            "secure_p": "GPhone",
            "req_sn": round(time.time()*1000)
        }
        # 抽奖删除lottery_chance参数
        if type == 1: 
            del params["lottery_chance"]
        res = requests.get(url, params=params)
        print("（iqy）抽奖信息", res.json())
        if not res.json().get('code'):
            chance = int(res.json().get('daysurpluschance'))
            msg = res.json().get("awardName")
            return {"status": True, "msg": msg, "chance": chance}
        else:
            try:
                msg = res.json().get("kv", {}).get("msg")
            except:
                msg = res.json()["errorReason"]
            return {"status": False, "msg": msg, "chance": 0}




if __name__ == '__main__':
    P00001 = ""
    P00003 = ""

    # 签到
    obj = IQY(P00001, P00003)
    msg1 = obj.sign()

    # 抽奖
    chance = obj.draw(0)["chance"]
    if chance:
        msg2 = ""
        for i in range(chance):
            ret = obj.draw(1)
            msg2 += ret["msg"]+";" if ret["status"] else ""
    else:
        msg2 = "抽奖机会不足"

    # 日常任务
    obj.queryTask().joinTask()
    msg3 = obj.queryTask().getReward()

    msg = f"【爱奇艺签到】\n签到：{msg1}\n抽奖：{msg2}\n任务：{msg3}"
    print(msg)