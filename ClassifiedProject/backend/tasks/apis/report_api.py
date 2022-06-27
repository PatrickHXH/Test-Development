from ninja import Router,Query
from django.forms.models import model_to_dict
from django.db.utils import IntegrityError
from backend.common import response,Error
from tasks.apis.api_schema import TaskIn,ResultOut,ProjectIn
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

#报告列表2
@router.get("/list",auth=None,response=List[ResultOut])  #自定义分页必须加response
@paginate(CustomPagination)
def get_report_list(request,filters:ProjectIn=Query(...)):
    tasks = TestTask.objects.filter(project_id=filters.project_id,is_delete=0)
    report_list = []
    for task in tasks:
        print("task id =>",task.id)
        reports = TestResult.objects.filter(task_id=task.id).all()
        for report in reports:
            print("report id=>",report.id)
            report_list .append(report)
    return  report_list

#报告详情
@router.get("/{report_id}/detail",auth=None)
def report_detail(request,report_id:int):
    report = get_object_or_404(TestResult,id=report_id)
    report_add = model_to_dict(report)
    report_add.update({'create_time':report.create_time})
    return response(result=report_add)

#报告删除
@router.post("/{report_id}/delete",auth=None)
def report_delete(request,report_id:int):
    report = get_object_or_404(TestResult,id=report_id)
    report.delete()
    report.save()
    return response()