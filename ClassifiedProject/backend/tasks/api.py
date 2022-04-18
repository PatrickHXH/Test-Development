import hashlib

from ninja import Router,File
from django.forms.models import model_to_dict
from backend.common import response,Error
from backend.pagination import CustomPagination
from ninja.pagination import paginate,PageNumberPagination  #分页
from typing import List
from tasks.api_schema import TaskIn
from projects.models import Project
from cases.models import TestCase
from tasks.models import TestTask,TaskCaseRelevance,TestResult
from django.shortcuts import get_object_or_404
import os

router = Router(tags=["tasks"])

@router.post("/",auth=None)
def create_project(request,data:TaskIn):
    '''
    创建任务
    '''
    project = get_object_or_404(Project,id=data.projcet)
    task = TestTask.objects.create(project_id=project.id,name=data.name,describe=data.describe)
    cases = []
    for case in data.case:
        TaskCaseRelevance.objects.create(task_id=task.id,case_id=case)
        case = TestCase.objects.get(id=case)
        cases.append({"case":case.id,"module":case.module_id})
    task_dict = model_to_dict(task)
    task_dict["cases"] = cases
    return response(result=task_dict)
