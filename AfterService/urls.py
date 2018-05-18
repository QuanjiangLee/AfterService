"""AfterService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from serviceApp import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^verifyLogin/', views.verifyLogin),
	url(r'^userLoginOut/', views.userLoginOut),
	url(r'^index/$', views.index),
    url(r'^userIndex/$', views.index),
    url(r'^adminIndex/$', views.index),
    url(r'^index/home/$', views.index_home),
    url(r'^userIndex/home/$', views.home),
    url(r'^adminIndex/home/$', views.home),
    url(r'^index/phones_list/$', views.phones_list),
    url(r'^userIndex/phones_list/$', views.phones_list),
    url(r'^adminIndex/phones_list/$', views.phones_list),
    url(r'^index/servers_list/$', views.servers_list),
    url(r'^userIndex/servers_list/$', views.servers_list),
    url(r'^adminIndex/orders_manage/$', views.orders_manage),
    url(r'^userIndex/orders_manage/$', views.orders_manage),
    url(r'^userIndex/his_orders_list/$', views.his_orders_list),
    url(r'^adminIndex/his_orders_list/$', views.his_orders_list),
    url(r'^userIndex/user_info/$', views.user_info),
    url(r'^adminIndex/user_info/$', views.user_info),   
    url(r'^adminIndex/admin_update_phones/$', views.admin_update_phones), 
    url(r'^adminIndex/del_phone_item/$', views.del_phone_item),
    url(r'^index/about/$', views.about),
    url(r'^userIndex/about/$', views.about),
    url(r'^registerUser/', views.registerUser),
    url(r'^alert_user_info/', views.alert_user_info),
    url(r'^get_servers_form/', views.get_servers_form),
    url(r'^addorderlist/', views.addorderlist),
    url(r'^order_close/', views.order_close),
    url(r'^commit_html/', views.get_commit_html),
    url(r'^commitorder/', views.commitorder),
    url(r'^gradeorder/', views.gradeorder),
    url(r'^get_order_ma_count/', views.get_order_ma_count),
    url(r'^get_order_his_count/', views.get_order_his_count),
    url(r'^get_login_user/', views.get_login_user),
]
