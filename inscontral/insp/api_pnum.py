import requests, re, json, time, os, os.path, sys
from inscontral.insp.data import header, name


class apipnum():
    def __init__(self, session, pnum=''):
        self._session = session
        self.pnum = pnum
        # self.getnum()

    def getnum(self):
        pr = ''
        mobile = ''
        if self.pnum != '':
            self.pnum = self.pnum[3:]
            mobile = "&mobile=%s" % (self.pnum)
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=00174911907c855fcaa0268bac36011e10378af1&itemid=455' + mobile
        print(url)
        r = self._session.get(url, verify=False)
        if r.ok == True:
            pr = r.text
            pr = pr.split('|')
            print(pr)
            if pr[0] == 'success':
                self.pnum = pr[1]
                print("[*] Sucessful get num")
            else:
                if r.text == '2010':
                    self.pnum = self.pnum
                else:
                    self.pnum = r.text
                    print(self.pnum)
            # self._session.close()
        else:
            # self._session.close()
            print("[x] Unknown Error Occurs!")
        return self.pnum

    def getcode(self):
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=00174911907c855fcaa0268bac36011e10378af1&itemid=455&mobile=' + str(self.pnum)
        print(url)
        codere = ''
        r = self._session.get(url, verify=False)
        if r.ok == True:
            print("[*] Sucessful follow the user")
            pr = r.text.split('|')
            if pr[0] == 'success':
                coderetemp = pr[1].split(' ')
                coderetemp2 = ''
                for x in coderetemp:
                    if x.isdigit():
                        coderetemp2 = str(coderetemp2) + str(x)
                codere = coderetemp2
            print(pr)
            self._session.close()
        else:
            self._session.close()
            print("[x] Unknown Error Occurs!")
        time.sleep(5)
        return codere

    def getcodenum(self, phonenum):
        self.pnum = phonenum
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=00174911907c855fcaa0268bac36011e10378af1&itemid=455&mobile=' + self.pnum
        print(url)
        codere = ''
        r = self._session.get(url, verify=False)
        if r.ok == True:
            print("[*] Sucessful follow the user")
            pr = r.text.split('|')
            if pr[0] == 'success':
                coderetemp = pr[1].split(' ')
                coderetemp2 = ''
                for x in coderetemp:
                    if x.isdigit():
                        coderetemp2 = str(coderetemp2) + str(x)
                codere = coderetemp2
            print(pr)
            self._session.close()
        else:
            self._session.close()
            print("[x] Unknown Error Occurs!")
        time.sleep(5)
        return codere
