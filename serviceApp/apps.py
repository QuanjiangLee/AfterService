#from django.apps import AppConfig

#class MapappConfig(AppConfig):
#    name = 'serviceApp'
from serviceApp.DB_connect import DBMethods

def is_user_exist(userNo, passwd):
    values = (userNo, passwd)
    dbStr = "select Count(*), user_grant from serviceApp_userinf where user_name='{0}' and user_passwd=password('{1}');"
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

def get_user_grant(request):
    user_grant = {}
    if is_logined(request) is False:
        user_grant = "custom"
    elif is_logined(request) == 'user':
        user_grant = "user"
    elif is_logined(request) == 'admin':
        user_grant = "admin"
    else:
        user_grant = "custom"
    return user_grant

def register_user(userNo, passwd, user_sex="boy"):
    values = (userNo, passwd, user_sex)
    dbStr = "insert into serviceApp_userinf (user_name, user_nickname, user_grant, user_sex,image_path, user_mask,user_grades, user_passwd) values('{0}','{0}',0,'{2}','0','its a lazy man!',0.0, password('{1}'));"
    dbStr = dbStr.format( *values )
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def admin_add_phones(phoneName, fileName, phoneDesp, login_user):
    values = (phoneName, fileName, phoneDesp, login_user)
    dbStr = "insert into serviceApp_phonesinf (phone_name, image_path, phone_details, admin_id_id) values ('{0}','{1}','{2}', {3});"
    dbStr = dbStr.format( *values )
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def get_user_id(userName):
    values = (userName, )
    dbStr = "select user_id from serviceApp_userinf where user_name='{0}';"
    dbStr = dbStr.format( *values )
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret
