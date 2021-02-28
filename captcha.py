#!/usr/bin/env python
# coding:utf-8

import re
import requests
from hashlib import md5

class Captcha(object):

    def __init__(self):
        self.username = ''
        password = ''
        self.password = md5(password.encode('utf8')).hexdigest()
        self.soft_id = ''

        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        params = {
            'codetype': codetype,
            'file_base64': self.b64
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

    def decrypt_captcha(self, img):
        self.b64 = re.findall(r'data:image/png;base64,(.*)', img)[0]
        response = (self.PostPic(self.b64, 1902))
        print('Result: ' + response['pic_str'])
        return response['pic_str']