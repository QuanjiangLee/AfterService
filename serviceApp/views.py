import json
import time
import urllib
from urllib import parse
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from datetime import datetime
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from serviceApp.apps import *

# Create your views here.

def login(request):
    return render(request, 'login.html')

@csrf_exempt
def verifyLogin(request):
    if request.method == "GET":
        userNo = request.GET.get("userNo","")
        passwd = request.GET.get("passwd","")
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        userNo = data['userNo']
        passwd = data['passwd']
    print('userNo',userNo)
    print('passwd',passwd)
    user = authenticate(request,username = userNo, password = passwd)
    if user is not None:
        auth_login(request,user)
        sessionId=request.session.session_key 
        response = {'result':True, 'sessionId':sessionId}
        return HttpResponse(json.dumps(response), content_type='application/json;charset=utf-8')
    else:
        response = {'result':False, 'error': "username or password is error!"}
        return HttpResponse(json.dumps(response), content_type='application/json;charset=utf-8')

@csrf_exempt
def userLoginOut(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    logout(request)
    return HttpResponse(json.dumps({'ret':True}), content_type='application/json;charset=utf-8')

def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    hostList = myServerMap.objects.all()
    return render(request, 'index.html', {'hostList' : hostList})

@csrf_exempt
def addHost(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')
    hostName = data['hostName']
    hostIp = data['hostIp']
    hostPort = data['hostPort']
    print(hostName, hostIp, hostPort)
    try:
        myServerMap.objects.create(hostName=hostName, IPAddress=hostIp, hostPort=hostPort)
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps({'ret':True}), content_type='application/json;charset=utf-8')

@csrf_exempt
def delHost(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    hostId = data['hostId']
    print(hostId)
    ret = myServerMap.objects.filter(id=hostId).delete()
    print(ret)
    if ret[0] > 0:
        return HttpResponse(json.dumps({'ret':True}), content_type='application/json;charset=utf-8')
    else:
        HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')


@csrf_exempt
def updateHost(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    hostId = data['hostId']
    hostName = data['hostName']
    hostIp = data['hostIp']
    hostPort = data['hostPort']
    ret = myServerMap.objects.filter(id=hostId).update(hostName=hostName, IPAddress=hostIp, hostPort=hostPort)
    if ret > 0:
        return HttpResponse(json.dumps({'ret':True}), content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')  


@csrf_exempt
def filterHost(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "GET":
        keyWords = request.GET.get('keyWords','')
    print(keyWords)
    if keyWords != '' or keyWords !=None:
        hostList = myServerMap.objects.filter(hostName__icontains=keyWords)
    else:
        hostList = myServerMap.objects.all()
    return render(request, 'index.html', {'hostList' : hostList})