from ninja import Router
from backend.common import response, Error
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.sessions.models import Session
from users.api_schema import RegisterIn, LoginIn

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
@router.post("/login",auth=None)
def user_login(request,data:LoginIn):
    username = data.username
    password  = data.password
    if username == "" or password =="":
        return  response(error=Error.USER_OR_PAWD_NULL)
    else:
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            #auth.login登录保存session到表里
            auth.login(request,user)
            session = Session.objects.last()
            user_info = {
                "id": user.id,
                "username": user.username,
                "session":session.session_key
            }
            return  response(user_info)
        else:
            return response(error=Error.USER_OR_PAWD_EROOR)

@router.get("/bearer")
def bearer(request):
    """
    假设，必须要登录之后才能访问
    测试：获取session
    """
    return {"session": request.auth}
