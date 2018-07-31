from django.db import models
import django.utils.timezone as timezone


# Create your models here.
# class user(models.Model):
#    username = models.CharField(max_length=30, unique=True)
#    poststate = models.IntegerField(default=0)
#    creatstep = models.IntegerField(default=0)
#    errortimes = models.IntegerField(default=0)
#    lastsrc = models.CharField(max_length=50)
#    pwd = models.CharField(max_length=20)
#    profile = models.IntegerField(default=0)
#    emailverify = models.IntegerField(default=0)
#    phoneverify = models.IntegerField(default=0)
#    phonenum = models.CharField(max_length=20)
#    cookielogin = models.CharField(max_length=2000)


class UploadList(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='uploadlist')
    add_date = models.DateTimeField('add_date', default=timezone.now)
    selected = models.BooleanField(default=0)


class State(models.Model):
    state = models.CharField(max_length=10000)
    add_date = models.DateTimeField('add_date', default=timezone.now)


class UploadCaption(models.Model):
    id = models.AutoField(primary_key=True)
    add_date = models.DateTimeField('add_date', default=timezone.now)
    caption = models.CharField(max_length=10000)
    selected = models.BooleanField(default=0)


class ShopData(models.Model):
    id = models.AutoField(primary_key=True)
    add_date = models.DateTimeField('add_date', default=timezone.now)
    shopname = models.CharField(max_length=200)
    disable = models.BooleanField(default=0)


class ShopFollowerToken(models.Model):
    id = models.AutoField(primary_key=True)
    add_date = models.DateTimeField('add_date', default=timezone.now)
    rank_token = models.CharField(max_length=10000)
    nextmaxid = models.CharField(max_length=1000)
    shopid = models.IntegerField(default=0)
    userid = models.IntegerField(default=0)


class FollowerData(models.Model):
    id = models.AutoField(primary_key=True)
    add_date = models.DateTimeField('add_date', default=timezone.now)
    sftid = models.IntegerField(default=0)
    followername = models.CharField(max_length=200)
    followdata = models.CharField(max_length=10000)


class DeviceData(models.Model):
    id = models.AutoField(primary_key=True)
    add_date = models.DateTimeField('add_date', default=timezone.now)
    devicename = models.CharField(max_length=200)
    uploadable = models.BooleanField(default=0)
    followable = models.BooleanField(default=0)
    setprofileable = models.BooleanField(default=0)

