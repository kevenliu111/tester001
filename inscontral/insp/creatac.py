from inscontral.insp.register import register
from inscontral.insp.sql_iphp import sqlcont
from inscontral.insp.api_pnum import apipnum
import inscontral.sql_py
import requests
import json

def craatac():
    inscontral.sql_py.udstate('創建賬號：初始化')
    ses = requests.session()
    sq = sqlcont('kevenliu', '630901', 'insfl')
    proxy_use = '66.82.144.29:8080'
    phone = apipnum(ses)
    reg = register(proxy_use, ses, sq, phone)
    pnum = phone.getnum()
    rsu = pnum
    if pnum != '':
        inscontral.sql_py.udstate('創建賬號：已取得號碼開始創建')
        reg.creatnew(pnum)
        rsu = reg.run()
    else:
        inscontral.sql_py.udstate('創建賬號：無法取得號碼，創建失敗')
    return rsu
