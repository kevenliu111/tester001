# login and function
import account_info
import requests, re, json, time, os, os.path, sys
from data import header, name
from random import randint
from bs4 import BeautifulSoup
from proxy import proxy_pool

# 数据
user_list = account_info.account


class functions():
    def __init__(self, proxy, session):
        self.proxy = proxy
        self._session = session

    def like(self):
        likeurl = "https://www.instagram.com/web/likes/1781561095543136899/like/"

    def follow(self, userid):
        for i in userid:
            hadersstr = ''
            for j in self.read_cookies():
                hadersstr = hadersstr + j + '=' + self.read_cookies()[j] + '; '
            print(hadersstr)
            header['cookie'] = hadersstr
            header['X-csrftoken'] = self.read_cookies()["csrftoken"]
            self.id = self.get_userid(i)
            header['referer'] = self.user_profile
            #header['X-Instagram-AJAX'] = '1e82359e2670'
            followurl = "https://www.instagram.com/web/friendships/" + self.id + "/follow/"
            #print(self._session.cookies)
            self._session.headers = header
            self.read_cookies()
            r = self._session.post(followurl, verify=False)
            #print(self._session.cookies)
            #proxies=self.proxy
            if r.ok == True:
                print("[*] Sucessful follow the user", i)
                self._session.close()
            else:
                self._session.close()
                print("[x] Unknown Error Occurs!")

    def get_userid(self, userid):
        self._session.cookies = requests.utils.cookiejar_from_dict(self.read_cookies(), cookiejar=None, overwrite=True)
        self.user_profile = "https://www.instagram.com/" + str(userid) + '/'
        r = self._session.get(self.user_profile, verify=False)  # proxies=self.proxy
        id = r.text.split('\",\"show_suggested_profiles')[0].split('profilePage_')[-1]
        print(id)
        return id

    def save_cookies(self):
        global _session
        with open('./' + "cookiefile", 'w')as f:
            json.dump(self._session.cookies.get_dict(), f)  # _session.cookies.save()

    def read_cookies(self):
        # _session.cookies.load()
        # _session.headers.update(header_data)
        with open('./' + 'cookiefile')as f:
            cookie = json.load(f)
            self._session.cookies.update(cookie)
            return cookie
