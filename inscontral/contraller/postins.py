class Photo(object):
    def __init__(self, models, request):
        self.models = models
        self.request = request

    def upload(self):
        img = self.models.UploadList(img=self.request.FILES.get('img'))
        img.save()

    def delete(self):
        picid = self.request.POST.get('picid')
        print(picid)
        if picid != 'no':
            delre = self.models.UploadList.objects.filter(id=picid).delete()
            print('delre' + str(delre))

    def select(self):
        picid = self.request.POST.get('picid')
        print(picid)
        if picid != 'no':
            selre1 = self.models.UploadList.objects.filter().update(selected=False)
            selre2 = self.models.UploadList.objects.filter(id=picid).update(selected=True)
            print('selre1' + str(selre1) + 'selre2' + str(selre2))

    def page(self):
        imgs = []
        if not self.models.UploadList.objects.filter(selected=True).exists():
            if not self.models.UploadList.objects.filter().exists():
                tmp = ''
            else:
                picidtmp = self.models.UploadList.objects.filter().first()
                self.models.UploadList.objects.filter(id=picidtmp.id).update(selected=True)
        imgstmp = self.models.UploadList.objects.all()
        for i in imgstmp:
            dictmp = {'id': i.id, 'url': i.img.url, 'selected': i.selected}
            imgs.append(dictmp)
            print(i.img.url)
        return imgs

    def title(self):
        retitle = ''
        if self.models.UploadList.objects.filter(selected=True).exists():
            pictmp = self.models.UploadList.objects.filter(selected=True).first()
            retitle = '已選發佈图片編號：' + str(pictmp.id)
        else:
            retitle = '未選擇圖片！'
        return retitle


class Caption(object):
    def __init__(self, models, request):
        self.models = models
        self.request = request

    def upload(self):
        img = self.models.UploadCaption(caption=self.request.POST.get('caption'))
        img.save()

    def delete(self):
        picid = self.request.POST.get('picid')
        print(picid)
        if picid != 'no':
            delre = self.models.UploadCaption.objects.filter(id=picid).delete()
            print('delre' + str(delre))

    def select(self):
        picid = self.request.POST.get('picid')
        print(picid)
        if picid != 'no':
            selre1 = self.models.UploadCaption.objects.filter().update(selected=False)
            selre2 = self.models.UploadCaption.objects.filter(id=picid).update(selected=True)
            print('selre1' + str(selre1) + 'selre2' + str(selre2))

    def page(self):
        imgs = []
        if not self.models.UploadCaption.objects.filter(selected=True).exists():
            if not self.models.UploadCaption.objects.filter().exists():
                tmp = ''
            else:
                picidtmp = self.models.UploadCaption.objects.filter().first()
                self.models.UploadCaption.objects.filter(id=picidtmp.id).update(selected=True)
        imgstmp = self.models.UploadCaption.objects.all()
        for i in imgstmp:
            dictmp = {'id': i.id, 'caption': i.caption, 'selected': i.selected}
            imgs.append(dictmp)
            print(i.caption)
        return imgs

    def title(self):
        retitle = ''
        if self.models.UploadCaption.objects.filter(selected=True).exists():
            pictmp = self.models.UploadCaption.objects.filter(selected=True).first()
            retitle = '已選發佈图片編號：' + str(pictmp.id)
        else:
            retitle = '未選擇圖片！'
        return retitle


