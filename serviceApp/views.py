import json
import time
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from datetime import datetime
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
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
    user = is_user_exist(userNo, passwd)
    print('user is', user)
    if user[0][0] > 0:
        user_grant = user[0][1]
        request.session["login_user"] = userNo
        request.session["user_grant"] = user_grant
        sessionId=request.session.session_key 
        print('sessionId is ',sessionId)
        print('user_grant is',user_grant)
        response = {'result':True, 'sessionId':sessionId, 'user_grant':user_grant}
        return HttpResponse(json.dumps(response), content_type='application/json;charset=utf-8')
    else:
        response = {'result':False, 'error': "用户名或密码不正确!"}
        return HttpResponse(json.dumps(response), content_type='application/json;charset=utf-8')


@csrf_exempt
def userLoginOut(request):
    try:
        del request.session['login_user']
        del request.session['user_grant']
    except KeyError:
        pass
    return HttpResponse(json.dumps({'ret':True}), content_type='application/json;charset=utf-8')

def index(request):
    if is_logined(request) is False:
        cusInfo = {'hello':'unknow', "user_grant":"custom"}
        return render(request, 'index.html',{'cusInfo':cusInfo})
    if is_logined(request) == 'user':
        userInfo = {'hello':'user',"user_grant":'user'}
        return render(request, 'userIndex.html', {'userInfo' : userInfo})
    if is_logined(request) == 'admin':
        adminInfo = {'hello':'admin', "user_grant":'admin'}
        return render(request, 'adminIndex.html', {'adminInfo' : adminInfo})

@csrf_exempt
def registerUser(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')
    try:
        userNo = data['userNo']
        passwd = data['passwd']
        print(userNo, passwd)
        if register_user(userNo,passwd):
            return HttpResponse(json.dumps({'ret':True}), content_type='application/json;c:harset=utf-8')
        else:
            return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')
    except Exception as err:
        print(str(err))
        return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')

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
