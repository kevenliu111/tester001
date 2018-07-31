from function import functions
from register import register
from proxy import proxy_pool, get_one_from_pool
from login import login
from login2 import login2
from get_flower import getfollower
from sql_iphp import sqlcont
from api_pnum import apipnum
from get_email import getemail
import requests
import json


ses = requests.session()
sq = sqlcont('kevenliu', '630901', 'insfl')
# pool=proxy_pool(1)
# proxy_use=get_one_from_pool(pool)
#sq.proxies = {'http': 'http://66.82.144.29:8080', 'https': 'http://66.82.144.29:8080'}
proxy_use = '66.82.144.29:8080'

#print(sq.getdatauser())
phone = apipnum(ses)
reg = register(proxy_use, ses, sq, phone)
pnum = phone.getnum()
if pnum != '':
    reg.creatnew(pnum)
    rsu = reg.run

#checkurl = ''

#emailv = sq.get_user_eamil();

#gmail = getemail()
#checkurl = gmail.get_checkurl(emailv['content']['email'], emailv['content']['password'])
#logintest = login(proxy_use, [[emailv['content']['username'], emailv['content']['pwd']]], ses, sq)
#logintest.run()
#logintest.email_check(checkurl)


    #print(ret)

#logintest = login2(proxy_use, [['kevenlau111', '630901']], ses)
#logintest.run()
#print(sq.insertuser('1111', '2222', 'n725er@163.com'))

print(sq.getemail())
#test111=register(proxy_use,ses)
#test111.run()


#logintest = login(proxy_use, 'urhkpost10016', '13513566', ses, sq)
#logintest.run()
#getfo = getfollower(proxy_use, ses,sq, logintest.u_name)
#getfo.getfollow('serco.storee')
#sq.close()
# print(test111)
