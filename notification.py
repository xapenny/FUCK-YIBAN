#daily.py
# coding=utf-8
import requests
import os
import urllib.request
import json as js
import urllib
import urllib.parse

settings = []
with open('settings.json','r',encoding='utf-8') as setting_file:
    settings = eval(setting_file.read())
    setting_file.close()

class MiraiBot:

    def __init__(self):
        self.botqq = ''
        self.adminqq = ''
        self.botauthkey = ''
        self.botaddr = ''
        session = self.get_session()
        self.session_code = session[0]
        self.session_body = session[1]
        
    def get_session(self):
        # Setup tunnel
        response = requests.get(self.botaddr + '/about')
        rt1=str(response.text)
        ver = rt1[-9:-3]
        print('[Console] Mirai-Api-HTTP Version: ' + ver)
        body = '{"authKey":"' + self.botauthkey + '"}'
        response2 = requests.post(url=self.botaddr + '/auth', data=body)
        print('[Console] HTTP Status Code: ' + str(response2.status_code))
        # Gather session
        r2t = response2.text
        if r2t[8] == '0':
            session = r2t[21:-2]
            print('[Console] Session Code: ' + str(session))
        else:
            print(r2t[8])
        # Verify session
        session_body = '{"sessionKey":"' + session + '","qq":"' + self.botqq + '"}'
        response3 = requests.post(url=self.botaddr + '/verify', data=session_body)
        r3t = response3.text
        if r3t[8] == '0':
            print('[Console] [get_session] Successfully connected to Mirai-Api-HTTP server!\n')
        else:
            print('[Console] [get_session] Failed!')
            print(r3t)
        return session,session_body

    def release_session(self):
    #Session keys need to be released immediately everytime you finish the process
        response = requests.post(url=self.botaddr + '/release', data=self.session_body)
        rt = response.text
        if rt[8] == '0':
            print('[Console] [release_session] Successfully Released Session ID!')
        else:
            print('[Console] [release_session] Failed!')
        return 0

    def send_to_qq_group(self, data_body, qq_group_id, atall='0'):
        if str(atall) == '0':
            payload_body = '{"sessionKey":"' + self.session_code + '","target": ' + str(qq_group_id) + ''',"messageChain":[{"type": "Plain", "text":"''' + data_body + '"}]}'
        else:
            payload_body = '{"sessionKey":"' + self.session_code + '","target": ' + str(qq_group_id) + ''',"messageChain":[{"type": "AtAll"},{"type": "Plain", "text":"''' + data_body + '"}]}'
        response4 = requests.post(url=self.botaddr + '/sendGroupMessage', data=payload_body.encode('utf-8'))
        r4t = response4.text
        print(r4t.replace('{"code":','[Console] [send_group_mirai] Code: ').replace(',"msg":'," | Message: ").replace(',"messageId":',' | Message ID: ').replace('}',''))
        return 0
        
    def alert_admin(self, alert_payload):
        result = self.send_to_friend(alert_payload,self.adminqq)
        return result

    def send_to_friend(self, data_body, qq_id):
        payload_body = '{"sessionKey":"' + self.session_code + '","target": ' + str(qq_id) + ''',"messageChain":[{"type": "Plain", "text":"''' + data_body + '"}]}'
        response4 = requests.post(url=self.botaddr + '/sendFriendMessage', data=payload_body.encode('utf-8'))
        r4t = response4.text
        print(r4t.replace('{"code":','[Console] [send_group_mirai] Code: ').replace(',"msg":'," | Message: ").replace(',"messageId":',' | Message ID: ').replace('}',''))
        return 0

    def send_image_from_file(self, image_path, qq_id):
        url = self.botaddr + '/uploadImage'
        files = {'img': open(image_path, 'rb')}           
        data = {"sessionKey": self.session_code, "type": "friend"}
        response = requests.post(url, files=files, data=data)
        resp_orig = response.json()
        result = self.send_image_to_friend(resp_orig['imageId'], qq_id)
        return result
        
    def send_image_to_friend(self, data_body, qq_id):
        payload_body = '{"sessionKey":"' + self.session_code + '","target": ' + str(qq_id) + ''',"messageChain":[{"type": "Image", "imageId": "''' + data_body + '"}]}'
        print(payload_body)
        response4 = requests.post(url=self.botaddr + '/sendFriendMessage', data=payload_body.encode('utf-8'))
        r4t = response4.text
        print(r4t.replace('{"code":','[Console] [send_group_mirai] Code: ').replace(',"msg":'," | Message: ").replace(',"messageId":',' | Message ID: ').replace('}',''))
        return 0

class XiaoLzBot:

    def __init__(self):
        self.botqq = settings[0]['botqq']
        self.adminqq = settings[0]['adminqq']
        self.botauthkey = settings[0]['botauthkey'] #32bit MD5 encryption
        self.botaddr = settings[0]['botaddr']
        self.cookies = {'pass':self.botauthkey}

    def send_to_qq_group(self, data_body, qq_group_id):
        payload_body = 'fromqq=' + self.botqq + '&togroup=' + str(qq_group_id) + '&text=' + urllib.parse.quote(data_body)
        response4 = requests.post(url=self.botaddr + '/sendgroupmsg', data=payload_body.encode('utf-8'), cookies=self.cookies)
        r4t = response4.text
        print(payload_body)
        print(r4t)
        return 0

    def send_to_friend(self, data_body, qq_id):
        payload_body = 'fromqq=' + self.botqq + '&toqq=' + str(qq_id) + '&text=' + urllib.parse.quote(data_body)
        response4 = requests.post(url=self.botaddr + '/sendprivatemsg', data=payload_body.encode('utf-8'), cookies=self.cookies)
        r4t = response4.text
        return 0

    def send_image_to_friends(self, image_path, qq_id):
        payload_body = 'fromqq=' + self.botqq + '&toqq=' + str(qq_id) + '&fromtype=1&path=' + urllib.parse.quote(os.getcwd() + '\\' + image_path)
        response = requests.post(url = self.botaddr + '/sendprivatepic', data=payload_body, cookies=self.cookies)
        imageid = response.text.replace('\\','')[8:-2]
        self.send_to_friend(imageid, qq_id)
        return 0

class ServerChan:
    def __init__(self):
        self.serverchan_sckey = 'https://sc.ftqq.com/{}.send'.format(settings[1]['svc_key'])
    
    def send_wechat_message(self, payload):
        body = {
            "text" : "yiban_autoclock",
            "desp" : payload,
        }
        requests.get(url=self.serverchan_sckey, params=body)

class Bark:
    def __init__(self):
        self.pushkey = 'https://api.day.app/{}/'.format(settings[2]['bark_key'])
    
    def send_bark_alert(self, title, payload):
        body = self.pushkey + title + '/' + payload
        requests.get(url=body)