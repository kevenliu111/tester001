# ins robots, main script
# coding='utf-8'
# __author__=='0han'
# __email__=='0han@protonmail.com'
# __data__=='2017.8'
import requests, re, json, time, os, os.path, sys
from inscontral.insp.data import header, name
import inscontral.sql_py
from random import randint
from bs4 import BeautifulSoup


# 数据
class Challenge(object):
    def __init__(self, username, password, sql):
        self.u_name = username
        self._session = requests.session()
        self.sql = sql
        self.passwd = password
        inscontral.sql_py.udstate('賬號開始嘗試于網頁登錄！')

    def run(self):
        cookietmp = self.read_cookies()
        print(cookietmp)
        print('print(cookietmp)')
        if cookietmp == 0:
            inscontral.sql_py.udstate('賬號未于網頁登錄過：創建新登錄')
            print('2222')
            header['Accept-Language'] = 'en-US,zh-Hans-CN;q=0.8,zh-Hans;q=0.6,en-GB;q=0.4,en;q=0.2'
            header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
            self._session.get('https://www.instagram.com', verify=False, headers=header)
            self.save_cookies()
            cookietmp = self.read_cookies()
            hadersstr = ''
            for j in cookietmp:
                hadersstr = hadersstr + j + '=' + cookietmp[j] + '; '
            print(hadersstr)
            header['cookie'] = hadersstr
            header['X-csrftoken'] = cookietmp["csrftoken"]
            rre = self.login()
        else:
            print('1111')
            cookietmp = self.read_cookies()
            hadersstr = ''
            header['Accept-Language'] = 'en-US,zh-Hans-CN;q=0.8,zh-Hans;q=0.6,en-GB;q=0.4,en;q=0.2'
            header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
            for j in cookietmp:
                hadersstr = hadersstr + j + '=' + cookietmp[j] + '; '
            header['cookie'] = hadersstr
            r = self._session.get('https://www.instagram.com/'+self.u_name+'/', headers=header, verify=False)
            r.encoding = 'utf-8'
            print(r.text)
            rre = r.text
            inscontral.sql_py.udstate('賬號已于網頁登錄過：無需登錄')
        #rre = self.login()

        return rre

    def login(self):
        inscontral.sql_py.udstate('登錄開始')
        cookietmp = self.read_cookies()
        hadersstr = ''
        header['Accept-Language'] = 'en-US,zh-Hans-CN;q=0.8,zh-Hans;q=0.6,en-GB;q=0.4,en;q=0.2'
        header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
        for j in cookietmp:
            hadersstr = hadersstr + j + '=' + cookietmp[j] + '; '
        print(hadersstr)
        header['cookie'] = hadersstr
        header['X-csrftoken'] = cookietmp["csrftoken"]
        header['Referer'] = "https://www.instagram.com/accounts/login/"
        payload = self.create_ajax()
        r = self._session.post('https://www.instagram.com/accounts/login/ajax/', data=payload, headers=header,
                               verify=False)  # proxies=self.proxy
        r.encoding = 'utf-8'
        print(r.text)
        if r.ok == True:
            self.save_cookies()
            inscontral.sql_py.udstate('登錄結果：' + r.text)
            print("[*] Sucessful log in to the", self.u_name)
        else:
            inscontral.sql_py.udstate('登錄結果：登錄失敗：' + r.text)
            print("[x] Unknown Error Occurs!")

        return r.text



    def create_ajax(self):
        r_data = {
            'username': self.u_name,  # username
            'password': self.passwd,  # password
            'queryParams': "{}"
        }
        return r_data


    def email_check(self, checkurl):
        hadersstr = ''
        cookie = self.read_cookies()
        for j in cookie:
            hadersstr = hadersstr + j + '=' + cookie[j] + '; '
        print(hadersstr)
        header['cookie'] = hadersstr
        header['X-csrftoken'] = self.read_cookies()["csrftoken"]
        header['referer'] = 'http://mail.163.com/js6/read/readhtml.jsp?mid=361:xtbBaRL041XlligHwQABsl&font=15&color=064977'
        followerurl = checkurl
        self._session.headers = header
        r = self._session.get(followerurl, verify=False)
        r.encoding = 'utf-8'
        if r.ok == True:
            print("[email_check] Susses:")
            print(r.text)
            self._session.close()
        else:
            self._session.close()
            print("[email_check] Unknown Error Occurs!")


    def save_cookies(self):
        #hascookies = False
        #with open('./' + "cookiefile", 'w')as f:
            #tesla = self._session.cookies.get_dict()
            # tesla['rur'] = 'FTW'
            #print(self._session.cookies)
         #   json.dump(self._session.cookies.get_dict(), f)  # _session.cookies.save()
        cookie = self._session.cookies.get_dict()
        print(cookie)
        cookieg = self.read_cookies()
        if cookieg == 0:
            hascookies = self.sql.save_cookie(self.u_name, json.dumps(cookie))
        else:
            for key, value in cookie.items():
                #print(key not in cookieg.keys())
                if ( (key not in cookieg.keys()) or (cookieg[key] != value) ):
                    cookieg[key] = value
            hascookies = self.sql.save_cookie(self.u_name, json.dumps(cookieg))
        return hascookies

    def read_cookies(self):
        # _session.cookies.load()
        # _session.headers.update(header_data)
        #with open('./' + 'cookiefile')as f:
        #    cookie = json.load(f)
        #    self._session.cookies.update(cookie)
        cookie = json.loads(self.sql.get_cookie(self.u_name)['content'])
        print(cookie)
        return cookie
