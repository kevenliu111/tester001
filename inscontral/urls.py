from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('acinfo/', views.acinfo, name='acinfo'),
    path('creatac/', views.creatac, name='creatac'),
    path('uploadimg/', views.uploadImg, name='uploadimg'),
    path('showimg/', views.showImg, name='showimg'),
    path('setuppro/', views.setuppro, name='setuppro'),
    path('loginweb/', views.loginweb, name='loginweb'),
    path('insuploadphoto/', views.insuploadphoto, name='insuploadphoto'),
    path('ugstate/', views.ugstate, name='ugstate'),
    path('ffollow/', views.ffollow, name='ffollow'),
    path('getloadimg/', views.getloadImg, name='getloadimg'),
    path('acinfoedit/', views.acinfoedit, name='acinfoedit'),
    path('shopinfo/', views.shopinfo, name='shopinfo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)