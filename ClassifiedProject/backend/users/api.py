from ninja import Router
from backend.common import response, Error
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.sessions.models import Session
from users.api_schema import RegisterIn, LoginIn,LoginOut
import pickle
import base64
import json
router = Router(tags=["users"])

#注册功能
@router.post("/register",auth=None)
def user_register(request,payload:RegisterIn):
    if payload.password != payload.confirm_password:
        return response(error=Error.PAWD_ERROR)
    try:
        User.objects.get(username=payload.username)
    except User.DoesNotExist:
        pass
    else:
        return response(error=Error.USER_EXIST)
    user = User.objects.create_user(username=payload.username,password=payload.password)
    user_info = {
        "id": user.id,
        "username":user.username
    }
    return response(result=user_info)

#登录功能
# @router.post("/login",auth=None)
# def user_login(request,data:LoginIn):
#     username = data.username
#     password  = data.password
#     if username == "" or password =="":
#         return  response(error=Error.USER_OR_PAWD_NULL)
#     else:
#         user = auth.authenticate(username=username,password=password)
#         print(user)
#         if user is not None:
#             #auth.login登录保存session到表里
#             auth.login(request,user)
#             session = Session.objects.last()
#             user_info = {
#                 "id": user.id,
#                 "username": user.username,
#                 "session":session.session_key
#             }
#             return  response(result=user_info)
#         # result = user_info
#         else:
#             return response(error=Error.USER_OR_PAWD_EROOR)



# 登录功能test
@router.post("/login",auth=None)
def user_login(request,data:LoginIn):
    username = data.username
    password  = data.password
    if username == "" or password =="":
        return  response(error=Error.USER_OR_PAWD_NULL)
    else:
        user = auth.authenticate(username=username,password=password)
        print(user)

        if user is not None:
            #auth.login登录保存session到表里
            a = auth.login(request,user)
            session = Session.objects.last()
            # s = []
            # for s in session:
            #     obj = json.loads(s.session_data.decode('base64')[41:])
            #     print(obj["_auth_user_id"])
            # session_list = []
            # get_effective_session(session_list)
            # print(session_list)
            user_info = {
                "id": user.id,
                "username": user.username,
                "session":session.session_key
            }
            return  response(result = user_info)
        else:
            return response(error=Error.USER_OR_PAWD_EROOR)

#退出登录功能
@router.post("/logout",auth=None)
def user_logout(request):
    #退出登陆
    auth.logout(request)
    return  response(result="退出登陆成功")

@router.get("/bearer",auth=None)
def bearer(request):
    """
    假设，必须要登录之后才能访问
    测试：获取session
    """
    # return {"session": request.auth}
    from django.core import signing
    value = signing.dumps({"foo": "bar"})
    src = signing.loads(value)
    print(value)
    print(src)
    return  response()