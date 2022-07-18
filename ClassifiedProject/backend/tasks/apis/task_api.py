import json
from ninja import Router, Query,Path
from django.forms.models import model_to_dict
from django.db.utils import IntegrityError
from backend.common import response,Error
from tasks.apis.api_schema import TaskIn,TaskOut,CaseLIstIn
from projects.models import Project
from cases.models import TestCase
from tasks.models import TestTask,TaskCaseRelevance
from django.shortcuts import get_object_or_404
import os
from backend.settings import BASE_DIR
from tasks.task_running.task_running import run2
from cases.apis.api_schema import ModuleIn,ProjectIn,CaseIn,CaseDebugIn,CaseAssertIn,CaseOut,ModuleSchema  #导入传参类
from typing import List  #分页用到的列表
from backend.pagination import CustomPagination   #自定义分页
from ninja.pagination import paginate,PageNumberPagination  #分页

data_dir = os.path.join(BASE_DIR,'tasks', '../task_running', 'test_data.json')
test_dir = os.path.join(BASE_DIR,'tasks', '../task_running', 'test_case.py')
router = Router(tags=["tasks_router"])

@router.post("/",auth=None)
def create_task(request,data:TaskIn):
    '''
    创建任务
    '''
    project = get_object_or_404(Project,id=data.project)
    task = TestTask.objects.create(project_id=project.id,name=data.name,describe=data.describe)
    cases = []
    # for case in data.case:
    #     TaskCaseRelevance.objects.create(task_id=task.id,case_id=case)
    #     case = TestCase.objects.get(id=case)
    #     cases.append({"case":case.id,"module":case.module_id})
    cases_json = json.dumps(data.cases)
    case_list = []
    for c in data.cases:
        case_list = case_list + c["casesId"]
    case_list_json = json.dumps(case_list)
    TaskCaseRelevance.objects.create(task_id=task.id, case=cases_json,case_list=case_list_json)
    task_dict = model_to_dict(task)
    task_dict["cases"] = cases
    return response(result=task_dict)

@router.post("/{task_id}/running",auth=None)
def start_task(request,task_id: int):
    '''
    执行任务
    '''
    task = get_object_or_404(TestTask,pk=task_id)
    task.status = 1
    task.save()
    run2(task_id)
    return response()

@router.get("/{task_id}",auth=None)
def get_task(request,task_id:int):
    '''
    获取任务详情
    '''
    task = get_object_or_404(TestTask,id=task_id)
    print(task)
    if task.is_delete is True:
        return  response(error=Error.TASK_DELETE_ERROR)
    relevance = TaskCaseRelevance.objects.get(task_id=task.id)
    # case_list = []
    # for r in relevance:
    #     case_list.append(r.case_id)
    task_dict = model_to_dict(task)
    task_dict['cases'] = json.loads(relevance.case)
    return  response(result=task_dict)

@router.post("/update/{task_id}", auth=None)
def update_case(request, task_id: int,  data: TaskIn):
    '''
    更新任务
    '''
    task = get_object_or_404(TestTask,id=task_id)
    task.name = data.name
    task.describe = data.describe
    task. save()

    case_list = []
    for case in data.cases:
        case_list = case_list + case["casesId"]

    relevance = TaskCaseRelevance.objects.get(task_id=task.id)
    relevance.case = json.dumps(data.cases)
    relevance.case_list = json.dumps(case_list)
    relevance.save()
    # relevance = TaskCaseRelevance.objects.filter(task_id=task_id)
    # relevance.delete()
    # cases = []
    # for case in data.case:
    #     try:
    #         TaskCaseRelevance.objects.create(task_id=task.id,case_id=case)
    #     except IntegrityError:
    #         return response(error=Error.CASE_DELETE_ERROR)
    #     case = TestCase.objects.get(pk=case)
    #     cases.append({
    #     "case" : case.id,
    #     "module": case.module_id
    #     })
    task_dict = model_to_dict(task)
    task_dict["cases"] = data.cases
    return response(result=task_dict)

#删除任务接口
@router.post("/delete/{task_id}", auth=None)
def delete_case(request, task_id: int):
    """
    删除任务
    auth=None 该接口不需要认证
    """
    task = get_object_or_404(TestTask, id=task_id)
    task.is_delete = True
    task.save()
    return response()

#任务列表接口
@router.get("/list/",auth=None,response=List[TaskOut])  #自定义分页必须加response
@paginate(CustomPagination)
def task_list(request,data:ProjectIn=Query(...)):
    print(data.project_id)
    return TestTask.objects.filter(project_id=data.project_id,is_delete=False).all()

# 获取任务下用例详情
@router.get("/{task_id}/caseList", auth=None)
def get_task_case_list(request, task_id: int):
    """
    获取任务详情
    auth=None 该接口不需要认证
    """
    relevance = get_object_or_404(TaskCaseRelevance,task_id=task_id)
    cases_list = json.loads(relevance.case_list)
    print(cases_list)
    cases_info =[]
    for case in cases_list:
        case_obj = TestCase.objects.get(id=case)
        cases_info.append(model_to_dict(case_obj))
    return response(result=cases_info)

#保存调整顺序的任务用例
@router.put("/{task_id}/caseList", auth=None)
def put_task_case_list(request, task_id: int,data:CaseLIstIn):
    """
    保存调整顺序的任务用例
    auth=None 该接口不需要认证
    """
    relevance = get_object_or_404(TaskCaseRelevance,task_id=task_id)
    relevance.case_list = json.dumps(data.caseList)
    relevance.save()
    return response(result=[])