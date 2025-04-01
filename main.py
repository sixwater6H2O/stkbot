from pypushdeer import PushDeer
import os
push_key = os.environ["PUSHDEER"]
ssycyx = os.environ["SSYCYX"]
cps = os.environ["CPS_ID"]
import requests
import time
import io,sys

pushdeer = PushDeer(pushkey=push_key)
    
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
            # print("未开播")
	    pushdeer.send_text("未开播"+self.upname+"直播间")
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
            if ssycyx in msg :
                # 获取发言
                if msg not in self.danmuset:
                    pushdeer.send_text("马在发弹幕："+self.upname+"直播间", desp=msg)
                    self.danmuset.append(msg)
                if len(self.danmuset)>50:
                    self.danmuset = self.danmuset[1:]
 

# 创建bDanmu实例
cps_list = cps.split(',')
cps_id = cps_list[::2]
cps_name = cps_list[1::2]
livehouse = []
for i in range(len(cps_id)):
    roomid = cps_id[i]
    upname = cps_name[i]
    livehouse.append(Danmu(roomid, upname))
i = 1
while i<=1:
    i += 1
    for live in livehouse:
        live.get_danmu()
        time.sleep(5)
 
