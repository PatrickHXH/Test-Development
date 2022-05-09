from ninja import  NinjaAPI

from users.api import router as users_router
from projects.api import router as projects_router
from cases.apis.module_api import router as modules_router
from cases.apis.case_api import router as cases_router
from tasks.apis.task_api import router as tasks_router
from tasks.apis.report_api  import router as reports_router
from ninja.security import HttpBearer
from django.contrib.sessions.models import Session
import  datetime


class InvalidSession(Exception):
    """无效的token"""
    pass
class OverdueSession(Exception):
    """过期的token"""
    pass

class GlobalAuth(HttpBearer):
    def authenticate(self, request, sessionkey):
        try:
            session = Session.objects.get(pk=sessionkey)
            expire_time = session.expire_date
            expire_time = expire_time.strftime("%Y-%m-%d %M:%H:%S")
            now = datetime.datetime.now().strftime("%Y-%m-%d %M:%H:%S")
            if expire_time < now:
                raise OverdueSession
        except Session.DoesNotExist:
            raise  InvalidSession
        else:
            return sessionkey


api = NinjaAPI(auth=GlobalAuth())

# 自定义异常，改变出现错误时返回值
@api.exception_handler(InvalidSession)
def on_invalid_session(request, exc):
    """无效session返回类型 """
    return api.create_response(request, {"detail": "Invalid session supplied"}, status=401)


@api.exception_handler(OverdueSession)
def on_overdue_session(request, exc):
    """过期session返回类型 """
    return api.create_response(request, {"detail": "Overdue session supplied"}, status=402)

api.add_router("/users/", users_router)
api.add_router("/projects/", projects_router)
api.add_router("/modules/", modules_router)
api.add_router("/cases/", cases_router)
api.add_router("/tasks/", tasks_router)
api.add_router("/reports/", reports_router)
