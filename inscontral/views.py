from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

import inscontral.insp.insphp_api
from inscontral.insp.sql_iphp import sqlcont
from inscontral.insp.creatac import craatac
from inscontral.insp.MyEncoder import MyEncoder
from inscontral.contraller import postins
from inscontral.insp.login import login
from django.forms.models import model_to_dict
import json, inscontral.models, inscontral.insp, requests, inscontral.sql_py, urllib.parse
from django.core.serializers.json import DjangoJSONEncoder


def index(request):
    sq = sqlcont('kevenliu', '630901', 'insfl')
    userdata = sq.getdatauser_name()
    inscontral.sql_py.udstate('無')
    sq.close()
    return render(request, 'index.html', {'userdata': userdata})


def account_info(request):
    userdata = ''
    return render(request, 'index.html', {'userdata': userdata})


def acinfo(request):
    sq = sqlcont('kevenliu', '630901', 'insfl')
    userdata = {}
    if request.is_ajax():
        sort = request.GET.get('sort')
        search = request.GET.get('search')
        order = request.GET.get('order')
        offset = request.GET.get('offset')
        limit = request.GET.get('limit')
        userdata['total'] = sq.getdatauser_all_count(search, sort, order, offset, limit)['total']
        userdata['rows'] = sq.getdatauser_all(search, sort, order, offset, limit)

    sq.close()
    return HttpResponse(json.dumps(userdata), content_type='application/json')


def shopinfo(request):
    shopdata = {}
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST.get('method') == 'creat':
                shopname = request.POST.get('shopname')
                sdd = inscontral.models.ShopData(shopname=shopname)
                sdd.save()
            elif request.POST.get('method') == 'edit':
                content = request.POST.get('content')
                field = request.POST.get('field')
                shopid = request.POST.get('id')
                print(content + field + shopid)
                if field == 'disable':
                    if content == 'True':
                        content = True
                    elif content == 'False':
                        content = False
                    inscontral.models.ShopData.objects.filter(id=shopid).update(disable=content)
            elif request.POST.get('method') == 'run':
                ca = inscontral.insp.insphp_api.getshopfollower()
        else:
            search = request.GET.get('search')
            order = request.GET.get('order')
            sort = request.GET.get('sort')

            if not sort or sort == '':
                sort = 'id'

            if order == 'asc':
                sort = '-' + sort

            offset = int(request.GET.get('offset'))
            limit = int(request.GET.get('limit'))
            data = []
            print(order + str(offset) + str(limit))
            imgstmp = inscontral.models.ShopData.objects.filter().order_by(sort)[offset:limit]
            print(imgstmp)
            for i in imgstmp:
                dictmp = {'id': i.id, 'shopname': i.shopname, 'add_date': str(i.add_date), 'disable': str(i.disable)}
                data.append(dictmp)
                # print(i.caption)
            shopdata['rows'] = data
            shopdata['total'] = 200

    return HttpResponse(json.dumps(shopdata), content_type='application/json')


def acinfoedit(request):
    sq = sqlcont('kevenliu', '630901', 'insfl')
    state = False
    if request.method == 'POST':
        content = request.POST.get('content')
        field = request.POST.get('field')
        userid = request.POST.get('id')
        print(content + field + userid)
        state = sq.updatauser_byid(userid, field, content)
    sq.close()
    return HttpResponse(json.dumps(state), content_type='application/json')


def creatac(request):
    # sq = sqlcont('kevenliu', '630901', 'insfl')
    ca = craatac()
    # sq.close()
    return HttpResponse(json.dumps(ca), content_type='application/json')


def setuppro(request):
    ca = ''
    if request.method == 'POST':
        ca = inscontral.insp.insphp_api.setprophoto()
    return HttpResponse(json.dumps(ca, cls=MyEncoder), content_type='application/json')


def ugstate(request):
    ca = 'no'
    if request.method == 'POST':
        state = request.POST.get('username')
        inscontral.sql_py.udstate(state)
        ca = 'ok'
    else:
        if request.method == 'GET':
            state = request.GET.get('state')
            ca = inscontral.sql_py.gdstate()
            # ca = serializers.serialize("json", ca)
            print(ca)
    return HttpResponse(json.dumps(ca), content_type='application/json')


def loginweb(request):
    lgwre = ''
    ca = ''
    collectiondata = ''
    if request.method == 'POST':
        sq = sqlcont('kevenliu', '630901', 'insfl')
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        phonenum = request.POST.get('phonenum')
        reflash = request.POST.get('reflash')
        print(username + reflash)
        # = requests.session()
        lgw = login(username, password, phonenum, sq)
        lgwre = lgw.run()

        print(lgwre)
        '''
        logdatatmp = sq.getdatauser_byname(username)
        if logdatatmp['content']['appcollectiontmp']:
            if reflash == 'true':
                sq.updatauser(username, 'loginset', '1')
                ca = inscontral.insp.insphp_api.loginphone()
                logdatatmp = sq.getdatauser_byname(username)
                print(logdatatmp['content'])
                collectiondata = json.loads(logdatatmp['content']['appcollectiontmp'].replace('\r\n', '\\r\\n'))
            else:
                collectiondata = json.loads(logdatatmp['content']['appcollectiontmp'].replace('\r\n', '\\r\\n'))
        else:
            sq.updatauser(username, 'loginset', '1')
            ca = inscontral.insp.insphp_api.loginphone()
            logdatatmp = sq.getdatauser_byname(username)
            print(logdatatmp['content'])
            collectiondata = json.loads(logdatatmp['content']['appcollectiontmp'].replace('\r\n', '\\r\\n'))
        '''
        sq.close()
    return HttpResponse(json.dumps(collectiondata, cls=MyEncoder), content_type='application/json', charset='utf-8')


def ffollow(request):
    ca = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        sq = sqlcont('kevenliu', '630901', 'insfl')
        sq.updatauser(username, 'first_follow', '3')
        ca = inscontral.insp.insphp_api.intfollow()
        sq.close()
    return HttpResponse(json.dumps(ca, cls=MyEncoder), content_type='application/json')


def uploadImg(request):
    if request.method == 'POST':
        img = inscontral.models.UploadList(img=request.FILES.get('img'))
        img.save()
    return render(request, 'uploadimg.html')


def showImg(request):
    imgs = inscontral.models.UploadList.objects.all()
    content = {
        'imgs': imgs,
    }
    for i in imgs:
        print(i.img.url)
    return render(request, 'showimg.html', content)


def getloadImg(request):
    redata = {}
    if request.method == 'POST':
        method = request.POST.get('method')
        pcmodel = request.POST.get('pcmodel')
        if pcmodel == 'photo':
            photoc = postins.Photo(inscontral.models, request)
            if method == 'upload':
                photoc.upload()

            elif method == 'delete':
                photoc.delete()

            elif method == 'select':
                photoc.select()

            imgs = photoc.page()
            redata['page'] = pcmodel
            redata['content'] = imgs
            redata['title'] = photoc.title()

        elif pcmodel == 'caption':
            captionc = postins.Caption(inscontral.models, request)
            if method == 'upload':
                captionc.upload()

            elif method == 'delete':
                captionc.delete()

            elif method == 'select':
                captionc.select()

            redata['page'] = pcmodel
            redata['content'] = captionc.page()
            redata['title'] = captionc.title()

        elif pcmodel == 'confrim':
            if not inscontral.models.UploadList.objects.filter(selected=True).exists():
                photoc = postins.Photo(inscontral.models, request)
                redata['page'] = 'photo'
                redata['content'] = photoc.page()
                redata['title'] = photoc.title()
            elif not inscontral.models.UploadCaption.objects.filter(selected=True).exists():
                captionc = postins.Caption(inscontral.models, request)
                redata['page'] = 'caption'
                redata['content'] = captionc.page()
                redata['title'] = captionc.title()
            else:
                sq = sqlcont('kevenliu', '630901', 'insfl')
                redata['page'] = 'confrim'
                redata['content'] = sq.searchdata('uploadset', '1')
                redata['title'] = '請確認發佈名單！確認后再次點擊發佈'

    return HttpResponse(json.dumps(redata, cls=MyEncoder), content_type='application/json')


def insuploadphoto(request):
    ca = ''
    if request.method == 'POST':
        ca = inscontral.insp.insphp_api.loadphoto()
    return HttpResponse(json.dumps(ca, cls=MyEncoder), content_type='application/json')


def followlike_byweb(request):
    redata = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        phonenum = request.POST.get('phonenum')
        ipsession = InstaPy(username=username, password=password)
        ipsession.login()
        # ipsession.set_user_interact(amount=1, randomize=True, percentage=50, media='Photo')
        ipsession.set_do_follow(enabled=True, percentage=40)
        ipsession.set_do_like(enabled=True, percentage=25)
        ipsession.interact_user_followers(['natgeo'], amount=10, randomize=True)
