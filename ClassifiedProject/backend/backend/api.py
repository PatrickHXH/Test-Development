from ninja import  NinjaAPI
from users.api import router as users_router
from projects.api import router as projects_router
from ninja.security import HttpBearer
from ninja.security import django_auth
from django.contrib.sessions.models import Session
import  datetime


class InvalidSession(Exception):
    """无效的session"""
    pass
class OverdueSession(Exception):
    """过期的session"""


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        '''
        自定义认证session处理
        '''
        try:
            session = Session.objects.get(pk=token)
            print("测试")
            # if seesion.expire_date < datetime.datetime.now():
            #     raise OverdueSession
        except Session.DoesNotExist:
            raise  InvalidSession
        else:
            return token


api = NinjaAPI(auth=GlobalAuth())

# 自定义异常，改变出现错误时返回值
@api.exception_handler(InvalidSession)
def on_invalid_session(request, exc):
    """无效session返回类型 """
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


@api.exception_handler(OverdueSession)
def on_overdue_session(request, exc):
    """过期session返回类型 """
    return api.create_response(request, {"detail": "Overdue session supplied"}, status=401)

api.add_router("/users/", users_router)
api.add_router("/projects/", projects_router)
