# register module
# coding='utf-8'
# __author__=='0han'
# __email__=='0han@protonmail.com'
# __data__=='17/5/2018'
import requests, re, json, time, os, os.path, sys
from inscontral.insp.data import header, name
from random import randint
from bs4 import BeautifulSoup
from inscontral.insp.proxy import proxy_pool
import inscontral.sql_py


class register():
    def __init__(self, proxy, session, sql, pn):
        # ipproxy,num
        self.proxy = proxy
        self._session = session
        self.sql = sql
        self.u_name = ''
        self.passwd = ''
        self.pnum = ''
        self.pn = pn
        self.smscode = ''
        self.client_id = ''
        print("==Instagram-accounts-generator==\n[*] start")  # 可以删除 deletable

    def creatnew(self, pnum):
        self.u_name = self.create_username()
        self.passwd = '13513566'
        self.sql.insertuser(self.u_name, self.passwd)
        self.pnum = '%s%s' % ('+86', pnum)
        self.sql.updatauser(self.u_name, 'phonenum', self.pnum)
        self.sql.updatauser(self.u_name, 'creatstep', '1')

        self._session.get('https://www.instagram.com', verify=False)
        self.save_cookies()

    def run(self):
        # print(222)
        inscontral.sql_py.udstate('創建賬號：初始化完成')
        cookie = self.read_cookies()
        hadersstr = ''
        for j in cookie:
            hadersstr = hadersstr + j + '=' + cookie[j] + '; '
        print(hadersstr)
        header['cookie'] = hadersstr
        header['X-csrftoken'] = cookie["csrftoken"]
        self.client_id = cookie["mid"]
        self.data = self.create_ajax()
        inscontral.sql_py.udstate('創建賬號：開始創建')
        ins = self.ins()
        insre = ''
        if ins['state']:
            self.updata_state('10')
            insre = 'Real Creat!'
            inscontral.sql_py.udstate('創建賬號：創建成功：賬號：' + self.u_name)
        else:
            if ins['step'] == 'sms':
                inscontral.sql_py.udstate('創建賬號：正在驗證SMS')
                smstmp = self.sms_send()
                if smstmp:
                    codetmp = self.sms_get()
                    if codetmp:
                        self.data = self.sms_data()
                        insms = self.ins()
                        insre = insms
                    else:
                        insre = 'Faill Get Sms!!!'
                        inscontral.sql_py.udstate('創建賬號：無法取得SMS，創建失敗')
            else:
                insre = ins['step']
                inscontral.sql_py.udstate('創建賬號：創建失敗：未知錯誤' + insre)

        time.sleep(5)
        return insre

    # print(111)
    def ins(self):
        cookie = self.read_cookies()
        hadersstr = ''
        for j in cookie:
            hadersstr = hadersstr + j + '=' + cookie[j] + '; '
        print(hadersstr)
        header['cookie'] = hadersstr
        header['X-csrftoken'] = cookie["csrftoken"]

        recreat = {}
        recreat['state'] = False
        header['Referer'] = 'https://www.instagram.com/accounts/emailsignup/'
        r = self._session.post('https://www.instagram.com/accounts/web_create_ajax/', data=self.data, headers=header,
                               verify=False)
        r.encoding = 'utf-8'
        if r.ok == True:
            res = json.loads(r.text)
            recreat['state'] = res['account_created']
            if recreat['state']:
                # self.save_account_info(self.u_name, self.passwd)
                # self.sql.insertuser(self.u_name, self.passwd, self.email)
                self.updata_state('10')
                print("[*] Sucessful create an account")
                self.save_cookies()
                inscontral.sql_py.udstate('創建賬號：創建成功：賬號：' + self.u_name)
                print(r.text)
            else:
                if res['error_type'] == 'form_validation_error':
                    recreat['step'] = 'sms'
                    # print("[*] Fail!!! form_validation_error!")
                    self.save_cookies()
                    print(r.text)
                else:
                    recreat['step'] = res['error_type']
                    # print("[*] Fail!!! create an account")
                    print(r.text)
            self._session.close()
        else:
            recreat['step'] = 'unknowfail'
            self._session.close()
            print("[x] Unknown Error Occurs!")

        return recreat

    def sms_get(self):
        self.sms_code = self.pn.getcode()
        smstimes = 0
        sg = False
        while self.sms_code == '':
            sg = True
            if smstimes % 15 == 0:
                self.sms_send()
            elif smstimes > 50:
                sg = False
                break
            self.sms_code = self.pn.getcode()
            smstimes = smstimes + 1
        return sg

    def sms_send(self):
        header['Referer'] = 'https://www.instagram.com/accounts/emailsignup/'
        data = {
            'client_id': self.client_id,
            'phone_number': self.pnum
        }
        print(data)
        r2 = self._session.post('https://www.instagram.com/accounts/send_signup_sms_code_ajax/', data=data,
                                headers=header,
                                verify=False)
        r2.encoding = 'utf-8'
        res2 = json.loads(r2.text)
        print(r2.text)
        return res2['sms_sent']

    def sms_data(self):
        r_data = {
            'password': self.passwd,  # password
            'phone_number': self.pnum,  # email for register
            'username': self.u_name,  #
            'first_name': self.u_name,  # 全名
            'sms_code': self.sms_code,
            'client_id': self.client_id,  #
            'seamless_login_enabled': 1,
            'tos_version': 'row'
        }
        print(self.pnum)
        print(self.passwd)
        # print(self.f_name)
        print(self.u_name)
        return r_data

    def create_username(self):
        # data = {'keyword': self.f_name, "numlines": "70", "formsubmit": "Generate Username"}
        # r = requests.post("http://namegenerators.org/username-generator/", data=data, verify=True)
        # r.encoding = 'utf-8'
        # soup = BeautifulSoup(r.text, 'html.parser')
        # result = soup.select(".section > div:nth-of-type(" + str(randint(1, 69)) + ")")[0].string
        # result = str(result) + "no" + str(randint(1, 20000))

        # return result
        return self.sql.newusername()['content']

    def updata_state(self, step):
        self.sql.updatauser(self.u_name, 'creatstep', step)

    def create_ajax(self):
        def get_emailaddress():
            # r = requests.get("https://10minutemail.net", verify=True)
            # r.encoding = 'utf-8'
            # soup = BeautifulSoup(r.text, 'html.parser')
            # return soup.input["value"]
            edre = self.sql.getemail()['content']
            return edre

        def generate_FullName():
            nameList = name['name']  # 储存在dic里的姓名数据
            namefornow = nameList[randint(1, 12)]
            return namefornow

        # self.email = get_emailaddress()['email']
        # self.phonenum =
        # self.epassword = get_emailaddress()['password']
        # self.f_name = generate_FullName()
        # self.passwd = self.f_name + 'password'
        # self.passwd = "13513566"
        # self.u_name = self.create_username()
        r_data = {
            'password': self.passwd,  # password
            'phone_number': self.pnum,  # email for register
            'username': self.u_name,  #
            'first_name': self.u_name,  # 全名
            'client_id': self.client_id,  #
            'seamless_login_enabled': 1,
            'tos_version': 'row'
        }
        print(self.pnum)
        print(self.passwd)
        # print(self.f_name)
        print(self.u_name)
        return r_data

    def save_cookies(self):
        # hascookies = False
        # with open('./' + "cookiefile", 'w')as f:
        # tesla = self._session.cookies.get_dict()
        # tesla['rur'] = 'FTW'
        # print(self._session.cookies)
        #   json.dump(self._session.cookies.get_dict(), f)  # _session.cookies.save()
        cookie = self._session.cookies.get_dict()
        cookieg = self.read_cookies()
        for key, value in cookie.items():
            # print(key not in cookieg.keys())
            if ((key not in cookieg.keys()) or (cookieg[key] != value)):
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

    def get_one_from_pool(self, pool, num):
        res = {}
        ipPool = pool
        res['https'] = ipPool[randint(0, num)]
        return res

    def save_account_info(self, username, password):
        with open("account_info.py", "a+") as a:
            a.write("\n['" + username + "','" + password + "'],")
