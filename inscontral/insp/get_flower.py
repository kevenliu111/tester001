import account_info
import requests, re, json, time, os, os.path, sys
from data import header, name
from random import randint
from bs4 import BeautifulSoup
from proxy import proxy_pool
from sql_iphp import sqlcont


# 数据
user_list = account_info.account


class getfollower():
    def __init__(self, proxy, session, sql, username):
        self.proxy = proxy
        self._session = session
        self.sql = sql
        self.username = username

    def getfollow(self, shopname):
        cookie = self.read_cookies()
        hadersstr = ''
        for j in cookie:
            hadersstr = hadersstr + j + '=' + cookie[j] + '; '
        print(hadersstr)
        header['cookie'] = hadersstr
        header['X-csrftoken'] = self.read_cookies()["csrftoken"]
        self.id = self.get_userid(shopname)
        header['referer'] = 'https://www.instagram.com/usainbolt/followers/'
        followerurl = "https://www.instagram.com/graphql/query/"
        self._session.headers = header
        gcheck = True
        while gcheck:
            tmpshop = self.sql.shopget('', shopname)
            print(tmpshop)
            if tmpshop['data']['end_cursor'] == '':
                payload = {'variables': '{"id":"' + self.id + '","first":24}', 'query_hash': '37479f2b8209594dde7facb0d904896a'}
            else:
                payload = {'variables': '{"id":"'+self.id+'","first":12'+',"after":"'+tmpshop['data']['end_cursor']+'"}', 'query_hash': '37479f2b8209594dde7facb0d904896a'}
            print(payload)
            r = self._session.get(followerurl,   params=payload,  verify=False)
            r.encoding = 'utf-8'
            if r.ok == True:
                print(r.text)
                tmptext = json.loads(r.text)
                if tmptext['status'] == 'ok':
                    self.save_follower(tmptext, shopname)
                    print("[*] Sucessful follow the user")
                    gcheck = tmptext['data']['user']['edge_followed_by']['page_info']['has_next_page']
                    time.sleep(5)
                    #self._session.close()
                else:
                    print('Follower Get Fail!!!!')
                    time.sleep(300)
            else:
                #self._session.close()
                #gcheck = False
                print(r.text)
                print("[x] Unknown Error Occurs!")
                time.sleep(300)




    def get_userid(self, userid):
        self._session.cookies = requests.utils.cookiejar_from_dict(self.read_cookies(), cookiejar=None, overwrite=True)
        self.user_profile = "https://www.instagram.com/" + str(userid) + '/'
        r = self._session.get(self.user_profile, verify=False)  # proxies=self.proxy
        id = r.text.split('\",\"show_suggested_profiles')[0].split('profilePage_')[-1]
        print(id)
        return id

    def save_cookies(self):
        #hascookies = False
        #with open('./' + "cookiefile", 'w')as f:
            #tesla = self._session.cookies.get_dict()
            # tesla['rur'] = 'FTW'
            #print(self._session.cookies)
         #   json.dump(self._session.cookies.get_dict(), f)  # _session.cookies.save()
        hascookies = self.sql.save_cookie(self.username, json.dumps(self._session.cookies.get_dict()))
        return hascookies

    def read_cookies(self):
        # _session.cookies.load()
        # _session.headers.update(header_data)
        #with open('./' + 'cookiefile')as f:
        #    cookie = json.load(f)
        #    self._session.cookies.update(cookie)
        cookie = json.loads(self.sql.get_cookie(self.username)['content'])
        return cookie

    def save_follower(self, data, shopname):
        #sq = sqlcont('kevenliu', '630901', 'insfl')
        self.sql.sqlinsert(data, shopname)
        #print(data)
        #with open('./' + 'followers', 'w')as f:
        #   f.write(data)


