import hashlib
import json
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
from backend.settings import BASE_DIR
from tasks.task_running.test_result import save_test_result

data_dir = os.path.join(BASE_DIR,'tasks','task_running','test_data.json')
test_dir = os.path.join(BASE_DIR,'tasks','task_running','test_case.py')
router = Router(tags=["tasks"])

@router.post("/",auth=None)
def create_task(request,data:TaskIn):
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

@router.post("/{task_id}/running",auth=None)
def start_task(request,task_id: int):
    '''
    执行任务
    '''
    task = get_object_or_404(TestTask,pk=task_id)
    Relevance = TaskCaseRelevance.objects.filter(task_id=task.id)
    list = []
    data = {}
    for rel in Relevance:
        try:
            case = TestCase.objects.get(id=rel.case_id,is_delete=False)
            # list.append(model_to_dict(case)
            params_body = case.params_body.replace("\'","\"")
            header = case.header.replace("\'","\"")
            header_dict = json.loads(header)
            params_body_dict = json.loads(params_body)
            data[case.name] = {
                "url": case.url,
                "method": case.method,
                "header": header_dict,
                "params_type": case.params_type,
                "params_body": params_body_dict,
                "assert_type": case.assert_type,
                "assert_text":case.assert_text
            }
        except TestCase.DoesNotExist:
            pass
    #写入测试用例至test_data.json
    print("1.写入测试用例至test_data.json")
    with open(data_dir,"w") as f:
        f.write(json.dumps(data,ensure_ascii=False))
    #执行测试用例
    print("2.执行测试用例")
    os.system(f"python {test_dir}")
    #保存测试结果
    save_test_result(task_id)
    return response()