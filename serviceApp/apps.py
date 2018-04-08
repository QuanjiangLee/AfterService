#from django.apps import AppConfig

#class MapappConfig(AppConfig):
#    name = 'serviceApp'
from serviceApp.DB_connect import DBMethods

def is_user_exist(userNo, passwd):
    values = (userNo, passwd)
    dbStr = "select Count(*), user_grant from serviceApp_userinf where user_name='{0}' and user_passwd='{1}';"
    dbStr = dbStr.format( *values )
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret

def is_logined(request):
    login_user=request.session.get('login_user',None)
    user_grant=request.session.get('user_grant',None)
    #print('login_user is',login_user)
    print('user_grant is',user_grant)
    if login_user is None:
        return False
    if user_grant == 1:
        return 'admin'
    elif user_grant == 0:
        return 'user' 
    return False