


# ------------------------------------------------------------------------
# 导入一些第三方包
# ------------------------------------------------------------------------
import requests
import time
import datetime
import sys
import json
import itchat
import numpy as np
import pandas as pd
from qcloudsms_py import TtsVoiceSender


# ------------------------------------------------------------------------
# 设置一些全局变量
# ------------------------------------------------------------------------

# 设置打印输出宽度、行高
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)


# 腾讯电话语音功能 key
app_id = '1400140464'
app_key = '6dcd4dbdcb4ef1fd923a769b862aec67'
tts_code = '196005'
tts_param1 = ['云智能锁', '提醒您,有好消息', '财神', '好运来,大涨']
tts_param2 = ['云智能锁', '提醒您,有报警', '财神', '好运来,小风险']
phone = '13818280291'


# ------------------------------------------------------------------------
# 定义一些函数
# ------------------------------------------------------------------------

# 微信文本通知
def send_webchat_message(user,message):
    users = itchat.search_friends(user)
    userName = users[0]['UserName']
    itchat.send(message, toUserName=userName)


# 微信图片发送
def send_webchat_image(user,file_name):
    users = itchat.search_friends(user)
    userName = users[0]['UserName']
    itchat.send_image(file_name, toUserName=userName)



# 钉钉文本通知
def send_dingding_message(append_message):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=7778610adbdc5341eed346985b39983846e61b82525e69fc51646168e72f1d9a' #这里填写你自定义机器人的webhook地址
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = "周五下午提交项目周报，大家记得填写呀~. " + append_message
    String_textMsg = { \
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                "130xxxxxxxx"                                    #如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 1                                         #如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)


# 腾讯电话语音通知
def phone_call_message(tts_param):
    global app_id
    global app_key
    global tts_code
    global phone
    voice = TtsVoiceSender(app_id, app_key)
    result = voice.send(tts_code, tts_param, phone)
    print(result)


def test():

    while 1:
        # 微信通知
        #itchat.auto_login(enableCmdQR=2, hotReload=True)
        #send_webchat_message("麒麟", "这是胡青松的测试机器人")

        # 钉钉通知
        send_dingding_message("这是胡青松的测试机器人")


        # 腾讯语音
        #tts_param1 = ['云智能锁', '提醒您,有好消息', '财神', '好运来,大涨']
        #phone_call_message(tts_param1)

        time.sleep(10)

