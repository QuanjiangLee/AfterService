import os
import json
import time
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from datetime import datetime
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from serviceApp.models import *
from serviceApp.apps import *

# Create your views here.

BASE_DIR =os.path.abspath('.')
UPLOAD_PATH = 'serviceApp/static/pic_folder'


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
    try:
        user = userInf.objects.get(user_name=userNo, user_passwd=passwd)
    except Exception as err:
        response = {'result':False, 'error': "用户名或密码不正确!"}
        return HttpResponse(json.dumps(response), content_type='application/json;charset=utf-8')  
    else:
        print('user is', user)
        if user:
            user_grant = user.user_grant
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
        return redirect('/index/home/')
        #return render(request, 'index.html',{'cusInfo':cusInfo})
    if is_logined(request) == 'user':
        #userInfo = {'hello':'user',"user_grant":'user'}
        return redirect('/userIndex/home/')
        #return render(request, 'userIndex.html', {'userInfo' : userInfo})
    if is_logined(request) == 'admin':
        #adminInfo = {'hello':'admin', "user_grant":'admin'}
        return redirect('/adminIndex/home')
        #return render(request, 'adminIndex.html', {'adminInfo' : adminInfo})

def home(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    user_grant = get_user_grant(request)
    if user_grant == "user":
        return render(request, 'home.html',{'extend': 'userIndex.html'})
    elif user_grant == "admin":
        login_user=request.session.get('login_user',None)
        admin_id = userInf.objects.filter(user_name=login_user).first()
        items = phonesInf.objects.filter(admin_id=admin_id)
        return render(request, 'admin_phones.html',{'extend': 'adminIndex.html', 'items':items})
    else:
        return redirect('/index/home/')

def index_home(request):
    return render(request, 'home.html',{'extend': 'index.html'})

'''
def redirect_to_user_home(request):
    return render(request, 'home.html',{'extend': 'userIndex.html'})

def redirect_to_admin_home(request):
    return render(request, 'admin_phones.html',{'extend': 'adminIndex.html'})
'''
def about(request):
    user_grant = get_user_grant(request)
    if user_grant == "custom":
        return render(request, 'about.html',{'extend': 'index.html'})
    elif user_grant == "user":
        return render(request, 'about.html',{'extend': 'userIndex.html'})
    else:
        return redirect('/index/home/')  


def phones_list(request):
    user_grant = get_user_grant(request)
    print(user_grant)
    if request.GET.get('type') == "html":
        items = phonesInf.objects.all()
        return render(request, 'select_phones_list.html',{'items':items})
    if user_grant == "custom":
        items = phonesInf.objects.all()
        return render(request, 'phones_list.html',{'extend': 'index.html', 'items':items, 'user_grant': user_grant})
    elif user_grant == "user":
        items = phonesInf.objects.all()
        return render(request, 'phones_list.html',{'extend': 'userIndex.html','items':items})
    else:
        login_user=request.session.get('login_user',None)
        admin_id = userInf.objects.filter(user_name=login_user).first()
        items = phonesInf.objects.filter(admin_id=admin_id)
        return render(request, 'admin_phones.html',{'extend': 'adminIndex.html', 'items':items}) 

def servers_list(request):
    user_grant = get_user_grant(request)
    if request.GET.get('type') == "html":
        items = userInf.objects.all().filter(user_grant=1)
        return render(request, 'select_servers_list.html',{'items':items})
    if user_grant == "custom":
        items = userInf.objects.all().filter(user_grant=1)
        return render(request, 'servers_list.html',{'extend': 'index.html','items':items, 'user_grant': user_grant}) 
    elif user_grant == "user":
        items = userInf.objects.all().filter(user_grant=1)
        return render(request, 'servers_list.html',{'extend': 'userIndex.html','items':items})

def orders_manage(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    user_grant = get_user_grant(request)
    if user_grant == "user":
        login_user=request.session.get('login_user',None)
        user=userInf.objects.get(user_name=login_user)
        lists = workOrders.objects.filter(user_id=user, order_status=0)
        return render(request, 'orders-manage.html',{'extend': 'userIndex.html','lists':lists, 'user_grant': user_grant}) 
    elif user_grant == "admin":
        login_user=request.session.get('login_user',None)
        user=userInf.objects.get(user_name=login_user)
        print(user)
        lists = workOrders.objects.filter(server_id=user, order_status=0)
        print(lists)
        return render(request, 'orders-manage.html',{'extend': 'adminIndex.html','lists':lists, 'user_grant': user_grant})
    else:
        return redirect('/index/home/')

def get_servers_form(request):
    return render(request, 'servers_form.html')

def get_commit_html(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    user_grant = get_user_grant(request)
    if request.method == "GET":
        order_id = request.GET.get('order_id',"")
        order_type = request.GET.get('order_type',"")
        if order_id:
            order = workOrders.objects.get(order_id=order_id)
            commit_title = order.order_title
            commit_Details = order.order_details
            print(commit_title)
            commits = commitDetails.objects.all().filter(commit_id=order)
            if order_type:
                order_type = order.order_status
                grade_status = order.grade_status
                order_grade = 0.0
                grade_details = None
                if grade_status == 1:
                    order_grade = order.order_grade
                    grade_details = gradesInf.objects.filter(grade_id=order_id).latest('grade_id').user_message
                return render(request, 'commit_html.html',{'commits':commits, 'commit_title': commit_title,'commit_Details':commit_Details, 'order_type':order_type,\
            'grade_status':grade_status, 'order_grade':order_grade, 'grade_details': grade_details,'user_grant':user_grant})
            else:
                return render(request, 'commit_html.html',{'commits':commits, 'commit_title': commit_title, 'commit_Details':commit_Details, 'user_grant':user_grant})
        else:
            return render(request, 'commit_html.html')

def his_orders_list(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    user_grant = get_user_grant(request)
    print(user_grant)
    if user_grant == "user":
        login_user=request.session.get('login_user',None)
        user=userInf.objects.get(user_name=login_user)
        lists = workOrders.objects.filter(user_id=user, order_status=1)
        return render(request, 'user_orders.html',{'extend': 'userIndex.html', 'lists':lists, 'user_grant': user_grant})
    elif user_grant == "admin":
        login_user=request.session.get('login_user',None)
        user=userInf.objects.get(user_name=login_user)
        lists = workOrders.objects.filter(server_id=user, order_status=1)
        return render(request, 'user_orders.html',{'extend': 'adminIndex.html', 'lists':lists, 'user_grant': user_grant})
    else:
        return redirect('/index/home/')

def user_info(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    user_grant = get_user_grant(request)
    login_user=request.session.get('login_user',None)
    user_id = userInf.objects.get(user_name=login_user).user_id
    if user_grant == "user":
        user_info = userInf.objects.filter(user_id=user_id)
        return render(request, 'user_info.html',{'extend': 'userIndex.html','user_info': user_info[0],'user_grant':user_grant})
    elif user_grant == "admin":
        user_info = userInf.objects.filter(user_id=user_id)
        return render(request, 'user_info.html',{'extend': 'adminIndex.html','user_info': user_info[0],'user_grant':user_grant})
    else:
        return redirect('/index/home/')

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
        ret = userInf.objects.filter(user_name=userNo)
        if ret:
            return HttpResponse(json.dumps({'ret':'registered'}), content_type='application/json;charset=utf-8')
        else:
            ret = userInf.objects.create(user_name=userNo, user_nickname=userNo, user_grant=0, user_sex="男", user_mask="这个人太懒了！",user_grades=0.0, user_passwd=passwd)
            if ret:
                return HttpResponse(json.dumps({'ret':True}), content_type='application/json;c:harset=utf-8')
            else:
                return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')
    except Exception as err:
        print(str(err))
        return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')

@csrf_exempt
def admin_update_phones(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    print(request.FILES)
    file_data = None
    if request.FILES:
        file_data = request.FILES['choosefile']
        print(file_data)
    phoneName = request.POST.get("phoneName", "")
    phoneDesp = request.POST.get("phoneDesp", "")
    type = request.POST.get("type", "")
    print(type)
    
    file_path = os.path.join(BASE_DIR, UPLOAD_PATH)
    print(file_path)
    if file_data: 
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        #print(file_path)
        #print(file_data.name)
        full_path = os.path.join(file_path, file_data.name)
        #print(full_path)
        try:
            fw = open(full_path, 'wb+')
        except:
            ret = False
            return HttpResponse(json.dumps(ret), content_type='application/json')
        for fd in file_data:
            fw.write(fd)
        fw.close()
        if not os.path.exists(full_path):
            ret = False
            return HttpResponse(json.dumps(ret), content_type='application/json')               
    if type == 'alter':
        phone_id = request.POST.get("phoneId", "")
        if file_data:
            ret = phonesInf.objects.filter(phone_id=phone_id).update(phone_name=phoneName,image_path=file_data.name, phone_details=phoneDesp)
        else:
            ret = phonesInf.objects.filter(phone_id=phone_id).update(phone_name=phoneName, phone_details=phoneDesp)
        if ret > 0:
            return HttpResponse(json.dumps({'ret':True}), content_type='application/json;charset=utf-8')
        else:
            return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')
    elif type == 'add':
        login_user=request.session.get('login_user',None)
        user = userInf.objects.get(user_name=login_user)
        ret = phonesInf.objects.create(phone_name=phoneName, image_path=file_data.name, phone_details=phoneDesp, admin_id=user)
        #print('ret', ret)
        if ret:
            return HttpResponse(json.dumps(True), content_type='application/json')

@csrf_exempt
def alert_user_info(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        userName = data['userName']
        userSex = data['userSex']
        userMark = data['userMark']
        print(userName, userSex, userMark)
        login_user=request.session.get('login_user',None)
        user_id = userInf.objects.get(user_name=login_user).user_id
        ret = userInf.objects.filter(user_id=user_id).update(user_nickname=userName,user_sex=userSex, user_mask=userMark)
        if ret > 0:
            return HttpResponse(json.dumps(True), content_type='application/json;charset=utf-8')
        else:
            return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    except Exception as err:
        print(str(err))
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')

@csrf_exempt
def addorderlist(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        login_user=request.session.get('login_user',None)
        user = userInf.objects.get(user_name=login_user)
        phone_id = data['phone_id']
        server_id = data['server_id']
        order_title = data['order_title']
        order_details = data['order_details']
        server = userInf.objects.get(user_id=server_id)
        print('server is ', server)
        phone = phonesInf.objects.get(phone_id=phone_id)
        workOrders.objects.create(user_id=user, server_id=server, phone_id=phone, order_title=order_title, order_details=order_details)
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps(True), content_type='application/json;charset=utf-8')


@csrf_exempt
def commitorder(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        order_id = data['order_id']
        commit_to_user = data['commit_to']
        commit_details = data['order_details']
        order = workOrders.objects.get(order_id=order_id)
        commit_to = userInf.objects.get(user_name=commit_to_user)
        login_user=request.session.get('login_user',None)
        commit_from = userInf.objects.get(user_name=login_user)
        commitDetails.objects.create(commit_id=order, commit_from = commit_from, commit_to = commit_to, commit_details=commit_details)
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps(True), content_type='application/json;charset=utf-8')

@csrf_exempt
def gradeorder(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        order_id = data['order_id']
        grade_for = data['grade_for']
        user_grade = data['order_grade']
        user_message = data['grade_details']
        order = workOrders.objects.get(order_id=order_id)
        grade_for = userInf.objects.get(user_name=grade_for)
        login_user=request.session.get('login_user',None)
        grade_from = userInf.objects.get(user_name=login_user)
        gradesInf.objects.create(grade_id=order, user_id=grade_from, server_id = grade_for, user_grade = user_grade, user_message=user_message)
        workOrders.objects.filter(order_id=order_id).update(grade_status=1,order_grade=user_grade)
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    else:
        grade = userInf.objects.get(user_id=grade_for.user_id).user_grades
        print(grade)
        cur_grade = 0.0
        if grade > 0.0:
            cur_grade = (grade + float(user_grade)) / 2.0
        else:
            cur_grade = user_grade
        try:
            userInf.objects.filter(user_id=grade_for.user_id).update(user_grades=cur_grade)
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
        return HttpResponse(json.dumps(True), content_type='application/json;charset=utf-8')

@csrf_exempt
def order_close(request):
    if is_logined(request) is False:
        return redirect('/index/home/')    
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        order_id = data['order_id']
        workOrders.objects.filter(order_id=order_id).update(order_status=1)
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps(True), content_type='application/json;charset=utf-8')

@csrf_exempt
def get_order_ma_count(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    admin_user=request.session.get('login_user',None)
    server_id = userInf.objects.get(user_name=admin_user)
    count = workOrders.objects.filter(server_id=server_id,order_status=False).count()
    return HttpResponse(json.dumps({"count": count}), content_type='application/json;charset=utf-8')

@csrf_exempt
def get_order_his_count(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    admin_user=request.session.get('login_user',None)
    server_id = userInf.objects.get(user_name=admin_user)
    count = workOrders.objects.filter(server_id=server_id,order_status=True).count()
    return HttpResponse(json.dumps({"count": count}), content_type='application/json;charset=utf-8')

@csrf_exempt
def get_login_user(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    cur_user = request.session.get('login_user',None)
    login_user = userInf.objects.get(user_name=cur_user).user_nickname
    if login_user:
        return HttpResponse(json.dumps({"login_user": login_user}), content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps({"login_user": None}), content_type='application/json;charset=utf-8')

@csrf_exempt
def addHost(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
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
def del_phone_item(request):
    if is_logined(request) is False:
        return redirect('/index/home/')
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    phoneId = data['phoneId']
    print(phoneId)
    ret = phonesInf.objects.filter(phone_id=phoneId).delete()
    print(ret)
    if ret[0] > 0:
        return HttpResponse(json.dumps({'ret':True}), content_type='application/json;charset=utf-8')
    else:
        HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')

