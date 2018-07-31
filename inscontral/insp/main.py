from function import functions
from register import register
from proxy import proxy_pool, get_one_from_pool
from login import login
from login2 import login2
from get_flower import getfollower
from sql_cont import sqlcont
from api_pnum import apipnum
import requests, time

ses = requests.session()
# pool=proxy_pool(1)
# proxy_use=get_one_from_pool(pool)
proxy_use = '192.168.6.1'
#print(proxy_use)
#logintest = login2(proxy_use, [['kevenlau111', '630901']], ses)
#logintest.run()
#fo = functions(proxy_use, ses)
#fo.follow(['counting.starr'])
# test111=register(proxy_use,ses)
# test111.run()
#getfo = getfollower(proxy_use, ses)
#getfo.getfollow('counting.starr')

phone = apipnum(ses)
phonenum = phone.getnum()
print(phonenum)
while True:
    pcode = phone.getcode()
    #print(phonenum)
    print(pcode)
    time.sleep(5)

# print(test111)
