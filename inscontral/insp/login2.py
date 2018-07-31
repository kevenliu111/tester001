# ins robots, main script
# coding='utf-8'
# __author__=='0han'
# __email__=='0han@protonmail.com'
# __data__=='2017.8'
import requests, re, json, time, os, os.path, sys
from data import header, name
from random import randint
from bs4 import BeautifulSoup
from proxy import proxy_pool


# 数据
class login2(object):
    def __init__(self, proxy, accountlist, session):
        self.list = accountlist
        self.proxy = proxy
        self._session = session

    def run(self):
        #self._session.get('https://www.instagram.com', verify=False)
        #self.save_cookies()
        #header['cookie'] = str(self.read_cookies())[1:-2]
        #header['X-csrftoken'] = self.read_cookies()["csrftoken"]
        header['User-Agent'] = 'Instagram 9.7.0 (iPhone6,1; iPhone OS 8_4; en_HK; en; scale=2.00; 640x1136) AppleWebKit/420+'
        header['Host'] = 'i.instagram.com'
        header['Accept-Encoding'] = 'gzip, deflate'
        header['Proxy-Connection'] = 'keep-alive'
        header['X-IG-Connection-Type'] = 'WiFi'
        header['X-IG-Capabilities'] = '3wo='
        header['Accept-Language'] = 'en;q=1, zh-Hans;q=0.9, zh-Hant;q=0.8'
        header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

        self.login()

    def login(self):
        for i in self.list:
            self.u_name = i[0]
            self.passwd = i[1]
            payload = self.create_ajax()
            r = self._session.post('https://i.instagram.com/api/v1/accounts/login/', data=payload, headers=header,
                                   verify=False)  # proxies=self.proxy
            print(r.text)
            if r.ok == True:
                self.save_cookies()
                print("[*] Sucessful log in to the", self.u_name)
            else:
                print("[x] Unknown Error Occurs!")

    def create_ajax(self):
        r_data = {
            'signed_body': 'f74dda6dbe7fc5a4b506193ef3ab8b66c0ac3a91e1b9ad57da6c5b799f62894d.{"username":"urhkpostaa","password":"13513566","device_id":"B8DEF6D2-8CE9-4E35-AB72-6434B6BFFFB1","login_attempt_count":"0"}',  # username
            'ig_sig_key_version': '5',  # password
        }
        return r_data

    def save_cookies(self):
        with open('./' + "cookiefile2", 'w')as f:
            #tesla = self._session.cookies.get_dict()
            # tesla['rur'] = 'FTW'
            #print(self._session.cookies)
            json.dump(self._session.cookies.get_dict(), f)  # _session.cookies.save()

    def read_cookies(self):
        # _session.cookies.load()
        # _session.headers.update(header_data)
        with open('./' + 'cookiefile2')as f:
            cookie = json.load(f)
            self._session.cookies.update(cookie)
            return cookie
