# ins robots, main script
# coding='utf-8'
# __author__=='0han'
# __email__=='0han@protonmail.com'
# __data__=='2017.8'
import requests, re, json, time, os, os.path, sys
from inscontral.insp.data import  name
import inscontral.sql_py
from inscontral.insp.api_pnum import apipnum
from random import randint
from bs4 import BeautifulSoup


# 数据
class login(object):
    def __init__(self, username, password, phonenum, sql):
        self.u_name = username
        self._session = requests.session()
        self.sql = sql
        self.passwd = password
        self.phonenum = phonenum
        inscontral.sql_py.udstate('賬號開始嘗試于網頁登錄！')
        self.header = {
            "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
            "accept-encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "cookie": None,
            "accept-language": "en-US,zh-Hans-CN;q=0.8,zh-Hans;q=0.6,en-GB;q=0.4,en;q=0.2",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/",
            "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
            "X-CSRFToken": None,
            "X-Requested-With": "XMLHttpRequest",
        }

    def run(self):

        cookietmp = self.read_cookies()
        print(cookietmp)
        print('print(cookietmp)')
        if cookietmp == 0:
            inscontral.sql_py.udstate(self.u_name + '賬號未于網頁登錄過：創建新登錄')
            print('2222')
            header = self.header
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
            header = self.header
            hadersstr = ''
            for j in cookietmp:
                hadersstr = hadersstr + j + '=' + cookietmp[j] + '; '
            header['cookie'] = hadersstr
            header['Referer'] = None
            header['origin'] = None
            header['Content-Type'] = None
            header['X-Requested-With'] = None
            r = self._session.get('https://www.instagram.com/' + self.u_name + '/', headers=header, verify=False,
                                  allow_redirects=False)
            r.encoding = 'utf-8'
            loc = ''
            rre = r.text
            print(r.text)
            self.save_cookies()
            if 300 <= r.status_code < 400:
                loc = r.headers['location']
                if loc == 'https://www.instagram.com/challenge/':
                    header['Referer'] = 'https://www.instagram.com/'
                    inscontral.sql_py.udstate(self.u_name + '二次驗證：需要驗證電話號碼！')
                    r2 = self._session.get(loc, headers=header, verify=False,
                                           allow_redirects=False)
                    r2.encoding = 'utf-8'
                    #print(r2.text)

                    if r2.ok == True:
                        xia = self.get_ajax(r2.text)
                        if xia != -1:
                            rre = self.challenge(xia)
                        else:
                            inscontral.sql_py.udstate(self.u_name+ '二次驗證：無法取得AJAX')
            else:

                soup = BeautifulSoup(r.text, 'lxml')
                var = soup.title.string.strip()
                print(var)
                if var == 'Page Not Found • Instagram':
                    inscontral.sql_py.udstate(self.u_name + '賬號失效，將自動刪除')
                    self.sql.updatauser(self.u_name, 'creatstep', '4')
                else:
                    inscontral.sql_py.udstate(self.u_name + '賬號已于網頁登錄過：無需登錄')
            # print(r.text)
            # rre = r.text

        # rre = self.login()

        return rre

    def challenge(self, cajax):
        cookietmp = self.read_cookies()
        hadersstr = ''
        header = self.header
        for j in cookietmp:
            hadersstr = hadersstr + j + '=' + cookietmp[j] + '; '
        print(hadersstr)
        header['cookie'] = hadersstr
        header['X-CSRFToken'] = cookietmp["csrftoken"]
        header['X-Instagram-AJAX'] = cajax
        header['Referer'] = "https://www.instagram.com/challenge/"
        payload = self.create_ajax_p()
        r = self._session.post('https://www.instagram.com/challenge/', data=payload, headers=header,
                               verify=False)  # proxies=self.proxy
        r.encoding = 'utf-8'
        print(r.text)
        rtext = json.loads(r.text)
        #print(rtext['challenge']['errors'][0])
        if rtext['status'] == 'ok' or (rtext['status'] == 'fail' and rtext['challenge']['errors'][0] == "This field is required."):
            smscode = self.sms_get()
            print(smscode)
            if smscode['state']:
                payload2 = self.create_ajax_vp(smscode['sms_code'])
                r2 = self._session.post('https://www.instagram.com/challenge/', data=payload2, headers=header,
                                        allow_redirects=False, verify=False)  # proxies=self.proxy
                if r2.ok == True:
                    rtext2 = json.loads(r2.text)
                    print(rtext2)
                    if rtext2['status'] == 'ok' and rtext2['type'] == 'CHALLENGE_REDIRECTION':
                        loc = rtext2['location']
                        if loc == 'https://www.instagram.com/':
                            inscontral.sql_py.udstate(self.u_name + '二次驗證：電話驗證成功！')
                            self.get_ins_index()
                    else:
                        inscontral.sql_py.udstate(self.u_name + '二次驗證：電話驗證失敗！' + r2.text)
                else:
                    inscontral.sql_py.udstate(self.u_name +'二次驗證：web請求失敗！' + r2.text)
            else:
                inscontral.sql_py.udstate(self.u_name + '二次驗證：SMS請求失敗！')
        else:
            inscontral.sql_py.udstate(self.u_name +'二次驗證：未知驗證請求：' + r.text)


    def login(self):
        inscontral.sql_py.udstate('登錄開始')
        header = self.header
        cookietmp = self.read_cookies()
        hadersstr = ''
        for j in cookietmp:
            hadersstr = hadersstr + j + '=' + cookietmp[j] + '; '
        print(hadersstr)
        header['cookie'] = hadersstr
        header['X-CSRFToken'] = cookietmp["csrftoken"]
        header['Referer'] = "https://www.instagram.com/accounts/login/"
        payload = self.create_ajax()
        r = self._session.post('https://www.instagram.com/accounts/login/ajax/', data=payload, headers=header,
                               verify=False)  # proxies=self.proxy
        r.encoding = 'utf-8'
        print(r.text)
        if r.ok == True:
            self.save_cookies()
            inscontral.sql_py.udstate(self.u_name + '登錄結果：' + r.text)
            print("[*] Sucessful log in to the", self.u_name)
        else:
            inscontral.sql_py.udstate(self.u_name + '登錄結果：登錄失敗：' + r.text)
            print("[x] Unknown Error Occurs!")

        return r.text


    def get_ins_index(self):
        print('1111')
        cookietmp = self.read_cookies()
        header = self.header
        hadersstr = ''
        for j in cookietmp:
            hadersstr = hadersstr + j + '=' + cookietmp[j] + '; '
        header['cookie'] = hadersstr
        header['Referer'] = None
        header['origin'] = None
        header['Content-Type'] = None
        header['X-Requested-With'] = None
        r = self._session.get('https://www.instagram.com/', headers=header, verify=False,
                              allow_redirects=False)
        r.encoding = 'utf-8'
        rre = r.text
        return rre


    def create_ajax(self):
        r_data = {
            'username': self.u_name,  # username
            'password': self.passwd,  # password
            'queryParams': "{}"
        }
        return r_data

    def create_ajax_p(self):
        r_data = {
            'phone_number': self.phonenum
        }
        return r_data

    def create_ajax_vp(self, security_code):
        r_data = {
            'phone_number': self.phonenum,
            'security_code': security_code
        }
        return r_data

    def get_ajax(self, xml):
        scri = -1
        soup = BeautifulSoup(xml, 'lxml')
        # print(soup.prettify())
        script = soup.find('script', text=re.compile("rollout_hash"))
        strscript = str(script.string)
        print(strscript)
        shax = strscript.find('rollout_hash')
        if shax != -1:
            rhaxs = shax + 15
            print(shax)
            ehax = strscript.find('"', rhaxs)
            print(ehax)
            scri = strscript[rhaxs:ehax]
        else:
            scri = -1
        return scri


    def sms_get(self):
        sgg = {}
        print(self.phonenum)
        pn = apipnum(self._session, self.phonenum)
        pncheck = pn.getnum()
        sgg['sms_code'] = ''
        smstimes = 0
        sgg['state'] = True
        while sgg['sms_code'] == '':
            sgg['state'] = True
            if pncheck == "2008":
                sgg['sms_code'] = ''
                smstimes = 0
                pn = apipnum(self._session)
                pnn = pn.getnum()
                self.phonenum = '%s%s' % ('+86', pnn)
                self.sms_reset()
                self.sql.updatauser(self.u_name, 'phonenum', self.phonenum)
                sgg['sms_code'] = pn.getcode()
                pncheck = ''
            elif smstimes % 15 == 0 and smstimes > 0:
                self.sms_replay()
            elif smstimes > 50:
                sgg['state'] = False
                break
            else:
                sgg['sms_code'] = pn.getcode()
            smstimes = smstimes + 1
        return sgg

    def sms_replay(self):
        resr = False
        cookietmp = self.read_cookies()
        hadersstr = ''
        header = self.header
        for j in cookietmp:
            hadersstr = hadersstr + j + '=' + cookietmp[j] + '; '
        print(hadersstr)
        header['cookie'] = hadersstr
        header['X-CSRFToken'] = cookietmp["csrftoken"]
        header['Referer'] = "https://www.instagram.com/challenge/"
        r = self._session.post('https://www.instagram.com/challenge/replay/',  headers=header,
                               verify=False)  # proxies=self.proxy
        if r.ok == True:
            print(r.text)
            #resrtmp = json.loads(r.text)
            #if resrtmp['state'] == 'ok':
            resr = True
        else:
            print(r.text)
        return resr



    def sms_reset(self):
        resr = False
        cookietmp = self.read_cookies()
        hadersstr = ''
        header = self.header
        for j in cookietmp:
            hadersstr = hadersstr + j + '=' + cookietmp[j] + '; '
        print(hadersstr)
        header['cookie'] = hadersstr
        header['X-CSRFToken'] = cookietmp["csrftoken"]
        header['Referer'] = "https://www.instagram.com/challenge/"
        r = self._session.post('https://www.instagram.com/challenge/reset/', headers=header,
                               verify=False)  # proxies=self.proxy

        if r.ok == True:
            resrtmp = json.loads(r.text)
            if resrtmp['status'] == 'ok':
                print(r.text)
                payload2 = self.create_ajax_vp('')
                r2 = self._session.post('https://www.instagram.com/challenge/', data=payload2, headers=header,
                                       verify=False)  # proxies=self.proxy
                if r2.ok == True:
                    resrtmp2 = json.loads(r2.text)
                    print(r2.text)
                    if resrtmp2['status'] == 'ok':
                        resr = True
                    else:
                        inscontral.sql_py.udstate('二次驗證：電話重置錯誤2001：' + r.text)
            else:
                inscontral.sql_py.udstate('二次驗證：電話重置錯誤1001：' + r.text)
        else:
            inscontral.sql_py.udstate('二次驗證：電話重置錯誤3001：' + r.text)
        return resr

    def email_check(self, checkurl):
        header = self.header
        hadersstr = ''
        cookie = self.read_cookies()
        for j in cookie:
            hadersstr = hadersstr + j + '=' + cookie[j] + '; '
        print(hadersstr)
        header['cookie'] = hadersstr
        header['X-CSRFToken'] = self.read_cookies()["csrftoken"]
        header[
            'referer'] = 'http://mail.163.com/js6/read/readhtml.jsp?mid=361:xtbBaRL041XlligHwQABsl&font=15&color=064977'
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
        # hascookies = False
        # with open('./' + "cookiefile", 'w')as f:
        # tesla = self._session.cookies.get_dict()
        # tesla['rur'] = 'FTW'
        # print(self._session.cookies)
        #   json.dump(self._session.cookies.get_dict(), f)  # _session.cookies.save()
        cookie = self._session.cookies.get_dict()
        print(cookie)
        cookieg = self.read_cookies()
        if cookieg == 0:
            hascookies = self.sql.save_cookie(self.u_name, json.dumps(cookie))
        else:
            for key, value in cookie.items():
                # print(key not in cookieg.keys())
                if ((key not in cookieg.keys()) or (cookieg[key] != value)):
                    if key != 'urlgen':
                        cookieg[key] = value
            hascookies = self.sql.save_cookie(self.u_name, json.dumps(cookieg))
        return hascookies

    def read_cookies(self):
        # _session.cookies.load()
        # _session.headers.update(header_data)
        # with open('./' + 'cookiefile')as f:
        #    cookie = json.load(f)
        #    self._session.cookies.update(cookie)
        cookie = json.loads(self.sql.get_cookie(self.u_name)['content'])
        print(cookie)
        return cookie
