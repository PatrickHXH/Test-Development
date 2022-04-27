from ninja import Router
from django.forms.models import model_to_dict
from django.db.utils import IntegrityError
from backend.common import response,Error
from tasks.apis.api_schema import TaskIn,ResultOut
from projects.models import Project
from cases.models import TestCase
from tasks.models import TestTask,TaskCaseRelevance,TestResult
from django.shortcuts import get_object_or_404
import os
from backend.settings import BASE_DIR
from tasks.task_running.task_running import run2
from typing import  List
from backend.pagination import CustomPagination
from ninja.pagination import paginate,PageNumberPagination

router = Router(tags=["reports_router"])

#报告列表
@router.get("/{task_id}/results",auth=None,response=List[ResultOut])  #自定义分页必须加response
@paginate(CustomPagination)
def report_list(request,task_id:int,**kwargs):
    task = get_object_or_404(TestTask,id=task_id)
    testresult = TestResult.objects.filter(task=task.id)
    return testresult

#报告详情
@router.get("/{report_id}/detail",auth=None)
def report_detail(request,report_id:int):
    report = get_object_or_404(TestResult,id=report_id)
    return response(result=model_to_dict(report))

#报告删除
@router.get("/{report_id}/delete",auth=None)
def report_delete(request,report_id:int):
    report = get_object_or_404(TestResult,id=report_id)
    report.delete()
    report.save()
    return response()