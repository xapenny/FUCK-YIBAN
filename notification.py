#daily.py
# coding=utf-8
from io import SEEK_CUR
import requests
import os
import time
import hashlib
import urllib.request
import json
import urllib
import urllib.parse

settings = []
with open('settings.json','r',encoding='utf-8') as _settings:
    settings = json.load(_settings)
    _settings.close()

class MiraiBot:

    def __init__(self):
        self.botqq = settings['qq']['botqq']
        self.adminqq = settings['qq']['adminqq']
        self.botauthkey = settings['qq']['botauthkey']
        self.botaddr = settings['qq']['botaddr']
        session = self.get_session()
        self.session_code = session[0]
        self.session_body = session[1]
        
    def get_session(self):
        """
        :说明：
            与MAH注册一条新连接
        """
        # Setup tunnel
        response = requests.get(self.botaddr + '/about')
        rt1=str(response.text)
        ver = rt1[-9:-3]
        print('[Console] Mirai-Api-HTTP Version: ' + ver)
        body = {"authKey": f"{self.botauthkey}"}
        response2 = requests.post(url=self.botaddr + '/auth', data=json.dumps(body))
        print(f'[Console] HTTP Status Code: {response2.status_code}')
        # Gather session
        r2t = response2.text
        if r2t[8] == '0':
            session = r2t[21:-2]
            print(f'[Console] Session Code: {session}')
        else:
            print(r2t[8])
        # Verify session
        session_body = {"sessionKey":f"{session}","qq":f"{self.botqq}"}
        response3 = requests.post(url=self.botaddr + '/verify', data=json.dumps(session_body))
        r3t = response3.text
        if r3t[8] == '0':
            print('[Console] [get_session] Successfully connected to Mirai-Api-HTTP server!\n')
        else:
            print('[Console] [get_session] Failed!')
            print(r3t)
        return session,session_body

    def release_session(self):
        """
        :说明：
            注销与MAH的连接
        """
        #Session keys need to be released immediately everytime you finish the process
        response = requests.post(url=self.botaddr + '/release', data=json.dumps(self.session_body))
        rt = response.text
        if rt[8] == '0':
            print('[Console] [release_session] Successfully Released Session ID!')
        else:
            print('[Console] [release_session] Failed!')
        return True

    def send_to_qq_group(self, data_body, qq_group_id, image=0, atall=0):
        """
        :说明：
            向QQ群发送消息
            `MAH`: `/sendGroupMessage`

        :参数：
            * ``data_body``: 待发送的文本内容
            * ``qq_group_id``: 目标QQ群号
            * ``image``: (可选)需要同时发送的本地图片文件
            * ``atall``: (可选)是否@全体成员
        """
        if atall:
            at_all = '{{"type": "AtAll"}},'
        else:
            at_all = ''
        if image:
            imageid = self._upload_image(image, 'group')
            image_payload = ',{{"type": "Image", "imageId": "{}"}}'.format(imageid)
        else:
            image_payload = ''
        payload_body = f"{{'sessionKey':'{self.session_code}','target': {qq_group_id},'messageChain':[{at_all}{{'type': 'Plain', 'text':'{data_body}'}}{image_payload}]}}"
        print(payload_body.encode('utf-8'))
        response4 = requests.post(url=self.botaddr + '/sendGroupMessage', data=json.dumps(eval(payload_body.encode('utf-8'))))
        r4t = response4.text
        print(r4t.replace('{"code":','[Console] [send_group_mirai] Code: ').replace(',"msg":'," | Message: ").replace(',"messageId":',' | Message ID: ').replace('}',''))
        return True

    def send_to_friend(self, data_body, qq_id, image=0):
        """
        :说明：
            向好友发送消息
            `MAH`: `/sendFriendMessage`

        :参数：
            * ``data_body``: 待发送的文本内容
            * ``qq_id``: 目标好友的QQ号
            * ``image``: (可选)需要同时发送的本地图片文件
        """
        if image:
            imageid = self._upload_image(image, 'friend')
            payload_body = f'{{"sessionKey":"{self.session_code}","target": {qq_id},"messageChain":[{{"type": "Plain", "text":"{data_body}"}},{{"type": "Image", "imageId": "{imageid}"}}]}}'
        else:
            payload_body = f'{{"sessionKey":"{self.session_code}","target": {qq_id},"messageChain":[{{"type": "Plain", "text":"{data_body}"}}]}}'
        # payload_body = '{"sessionKey":"' + self.session_code + '","target": ' + str(qq_id) + ''',"messageChain":[{"type": "Plain", "text":"''' + data_body + '"}]}'
        response4 = requests.post(url=self.botaddr + '/sendFriendMessage', data=json.dumps(eval(payload_body.encode('utf-8'))))
        r4t = response4.text
        print(r4t.replace('{"code":','[Console] [send_group_mirai] Code: ').replace(',"msg":'," | Message: ").replace(',"messageId":',' | Message ID: ').replace('}',''))
        return True

    def _upload_image(self, image_path, type):
        """
        :说明：
            上传本地图片 
            `MAH`: `/uploadImage`

        :参数：
            * ``image_path``: 本地图片路径
            * ``type``: 上传图片类型 (可选`friend`,`group`)
        """
        url = self.botaddr + '/uploadImage'
        files = {'img': open(image_path, 'rb')}           
        data = {"sessionKey": self.session_code, "type": f"{type}"}
        response = requests.post(url, files=files, data=data)
        resp_orig = response.json()
        return resp_orig['imageId']

class XiaoLzBot:

    def __init__(self):
        self.botqq = settings['qq']['botqq']
        self.adminqq = settings['qq']['adminqq']
        self.botauthkey = settings['qq']['botauthkey'] #32bit MD5 encryption
        self.botaddr = settings['qq']['botaddr']
        self.botpass = settings['qq']['botpass']
        #self.cookies = {'pass':self.botauthkey}

    def _get_cookie(self, operation):
        """
        :说明：
            获取Cookie

        :参数：
            * ``operation``: 小栗子HA事件
        """
        timestamp = str(int(time.time()))
        user = 'xapenny'
        exec_location = "{}{}".format(user, operation)
        passw = hashlib.md5(self.botpass.encode('utf-8')).hexdigest()
        authkey = hashlib.md5(str(exec_location+passw+timestamp).encode('utf-8')).hexdigest()
        cookies = {
            'user':user,
            'timestamp':timestamp,
            'signature':authkey
        }
        print(cookies)
        return cookies

    def send_to_qq_group(self, data_body, qq_group_id):
        """
        :说明：
            向QQ群发送消息
            ``operation``: ``/sendgroupmsg``

        :参数：
            * ``data_body``: 待发送的文本内容
            * ``qq_group_id``: 目标QQ群号
        """
        operation = '/sendgroupmsg'
        payload_body = 'logonqq=' + self.botqq + '&group=' + str(qq_group_id) + '&msg=' + urllib.parse.quote(data_body)
        cookie = self._get_cookie(operation)
        response4 = requests.post(url=self.botaddr + operation, data=payload_body.encode('utf-8'), cookies=cookie)
        r4t = response4.text
        return True

    def call_friend(self, dest_qq):
        """
        :说明：
            向好友拨打QQ电话
            ``operation``: ``/callfriend``

        :参数：
            * ``dest_qq``: 目标好友QQ
        """
        operation = '/callfriend'
        payload_body = 'logonqq=' + self.botqq + '&toqq=' + str(dest_qq)
        cookie = self._get_cookie(operation)
        response4 = requests.post(url=self.botaddr + operation, data=payload_body.encode('utf-8'), cookies=cookie)
        r4t = response4.text
        return True
    
    def send_like(self, dest_qq):
        """
        :说明：
            向好友发送名片赞
            ``operation``: ``/send_like``

        :参数：
            * ``dest_qq``: 目标好友QQ
        """
        operation = '/sendlike'
        payload_body = 'logonqq=' + self.botqq + '&toqq=' + str(dest_qq)
        cookie = self._get_cookie(operation)
        response4 = requests.post(url=self.botaddr + operation, data=payload_body.encode('utf-8'), cookies=cookie)
        r4t = response4.text
        return True

    def send_to_friend(self, data_body, qq_id):
        """
        :说明：
            向QQ好友发送消息
            ``operation``: ``/sendprivatemsg``

        :参数：
            * ``data_body``: 待发送的文本内容
            * ``qq_id``: 目标好友QQ号
        """
        operation = '/sendprivatemsg'
        payload_body = f"logonqq={self.botqq}&toqq={str(qq_id)}&msg={urllib.parse.quote(data_body)}"
        cookie = self._get_cookie(operation)
        response4 = requests.post(url=self.botaddr + operation, data=payload_body.encode('utf-8'), cookies=cookie)
        r4t = response4.text
        # print(r4t)
        return True

    def send_image_to_friends(self, image_path, qq_id, text=''):
        """
        :说明：
            向QQ好友发送包含图片的消息
            ``operation``: ``/sendprivatemsg``, ``/uploadfriendpic``

        :参数：
            * ``data_body``: 待发送的文本内容
            * ``qq_id``: 目标好友QQ号
            * ``text``: (可选)一起发送的文本内容
        """
        operation = '/uploadfriendpic'
        payload_body = 'logonqq=' + self.botqq + '&toqq=' + str(qq_id) + '&type=path&pic=' + urllib.parse.quote("{}\\".format(os.getcwd()) + image_path)
        cookie = self._get_cookie(operation)
        response = requests.post(url = self.botaddr + operation, data=payload_body, cookies=cookie)
        print(response.text)
        imageid = eval(response.text)['ret']
        self.send_to_friend(text+'\n'+imageid, qq_id)
        return True
    
    def send_image_to_group(self, image_path, qq_id, text=''):
        """
        :说明：
            向QQ群发送包含图片的消息
            ``operation``: ``/sendgroupmsg``, ``/uploadgrouppic``

        :参数：
            * ``data_body``: 待发送的文本内容
            * ``qq_id``: 目标QQ群号            
            * ``text``: (可选)一起发送的文本内容
        """
        operation = '/uploadgrouppic'  
        payload_body = 'logonqq=' + self.botqq + '&group=' + str(qq_id) + '&type=path&pic=' + urllib.parse.quote("{}\\".format(os.getcwd()) + image_path)
        cookie = self._get_cookie(operation)
        response = requests.post(url = self.botaddr + operation, data=payload_body, cookies=cookie)
        imageid = eval(response.text)['ret']
        self.send_to_qq_group(text+'\n'+imageid, qq_id)
        return True

class ServerChan:
    def __init__(self):
        self.serverchan_sckey = 'https://sc.ftqq.com/{}.send'.format(settings['wechat']['svc_key'])
    
    def send_wechat_message(self, payload):
        body = {
            "text" : "yiban_autoclock",
            "desp" : payload,
        }
        requests.get(url=self.serverchan_sckey, params=body)

class Bark:
    def __init__(self):
        self.pushkey = 'https://api.day.app/{}/'.format(settings['bark']['bark_key'])
    
    def send_bark_alert(self, title, payload):
        body = self.pushkey + title + '/' + payload
        requests.get(url=body)