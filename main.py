from pypushdeer import PushDeer
import os
push_key = os.environ["PUSHDEER"]
serverchan_key = os.environ["SERVERCHAN"]
sansheng = os.environ["SSYCYX"].split(',')
cps = os.environ["CPS"]
ssycyx = sansheng[0]
ss_room = sansheng[1]
import requests
import time
import io,sys

pushdeer = PushDeer(pushkey=push_key)

hders = {
            'Host': 'api.live.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        }
islive_data = {
            'room_id': ss_room,
        }
    
class Danmu():
    def __init__(self, roomid,upname):
        # 弹幕url
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
        # 请求头
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        }
        # 定义POST传递的参数
        self.data = {
            'roomid': roomid,
            'csrf_token': '',
            'csrf': '',
            'visit_id': '',
        }
        self.islive_url = "https://api.live.bilibili.com/room/v1/Room/get_info"
        self.islive_data = {
            'room_id': roomid,
        }
        self.danmuset = []
#         self.uinfo_url = "https://api.live.bilibili.com/live_user/v1/Master/info"
        self.upname=upname
 
    def get_danmu(self):
        # 获取直播间弹幕
        html = requests.post(url=self.url, headers=self.headers, data=self.data).json()
        info = requests.post(url=self.islive_url, headers=self.headers, data=self.islive_data).json()['data']
        status = info['live_status']
#         print(upname)
        if status!=1:
            # pushdeer.send_text("未开播"+self.upname+"直播间")
            return
        # 解析弹幕列表
        for content in html['data']['room']:
            # 获取昵称
            nickname = content['nickname']
#             upname = content['uname']
            text = content['text']
                # 获取发言时间
            timeline = content['timeline']
                # 记录发言
            msg = timeline + ' ' + nickname + ': ' + text
#             print(self.upname + ":"+ msg)
            if self.upname==ssycyx:
                if nickname in cps_name:
                # 获取发言
                    if msg not in self.danmuset:
                        title = nickname+"来了"
                        desp = msg
                        pushdeer.send_text(title, desp=desp)
                        sc_send(serverchan_key, title, desp)
                        self.danmuset.append(msg)
                    if len(self.danmuset)>50:
                        self.danmuset = self.danmuset[1:]
            if ssycyx in nickname :
                # 获取发言
                if msg not in self.danmuset:
                    title = "马在发弹幕："+self.upname+"直播间"
                    desp = msg
                    pushdeer.send_text(title, desp=desp)
                    sc_send(serverchan_key, title, desp)
                    self.danmuset.append(msg)
                if len(self.danmuset)>50:
                    self.danmuset = self.danmuset[1:]

import os
import requests
import re

def sc_send(sendkey, title, desp='', options=None):
    if options is None:
        options = {}
    # 判断 sendkey 是否以 'sctp' 开头，并提取数字构造 URL
    if sendkey.startswith('sctp'):
        match = re.match(r'sctp(\d+)t', sendkey)
        if match:
            num = match.group(1)
            url = f'https://{num}.push.ft07.com/send/{sendkey}.send'
        else:
            raise ValueError('Invalid sendkey format for sctp')
    else:
        url = f'https://sctapi.ftqq.com/{sendkey}.send'
    params = {
        'title': title,
        'desp': desp,
    }
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = requests.post(url, json=params, headers=headers)
    result = response.json()
    return result


# 创建bDanmu实例
cps_list = cps.split(',')
cps_id = cps_list[::2]
cps_name = cps_list[1::2]
cps_id.append(ss_room)
cps_name.append(ssycyx)
livehouse = []
for i in range(len(cps_id)):
    roomid = cps_id[i]
    upname = cps_name[i]
    livehouse.append(Danmu(roomid, upname))

from datetime import datetime, timedelta
start_time = time.time()
ssislive = 0
title = "运行开始"
desp = "可以手动关闭上次运行了"
pushdeer.send_text(title, desp=desp)
sc_send(serverchan_key, title, desp)
while True:
    try:
        info = requests.post(url="https://api.live.bilibili.com/room/v1/Room/get_info",
                         headers=hders, data=islive_data).json()['data']
        status = info['live_status']
        if status==1 and ssislive==0:
            ssislive = 1
            title = ssycyx+"开播了！"
            desp = info['live_time']+"\n直播标题："+info['title']
            pushdeer.send_text(title, desp=desp)
            sc_send(serverchan_key, title, desp)
        if status==0 and ssislive==1:
            ssislive = 0
        for live in livehouse:
            live.get_danmu()
            time.sleep(1)
        if (time.time()-start_time > 60*60*5):
            title = "运行结束"
            desp = "请检查下次定时是否正常开始"
            pushdeer.send_text(title, desp=desp)
            sc_send(serverchan_key, title, desp)
            break
    except Exception as e:
        # pushdeer.send_text("抓马代码报错", desp=str(e))
        continue
 
