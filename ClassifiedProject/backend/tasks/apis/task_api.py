from ninja import Router
from django.forms.models import model_to_dict
from django.db.utils import IntegrityError
from backend.common import response,Error
from tasks.apis.api_schema import TaskIn
from projects.models import Project
from cases.models import TestCase
from tasks.models import TestTask,TaskCaseRelevance
from django.shortcuts import get_object_or_404
import os
from backend.settings import BASE_DIR
from tasks.task_running.task_running import run2

data_dir = os.path.join(BASE_DIR,'tasks', '../task_running', 'test_data.json')
test_dir = os.path.join(BASE_DIR,'tasks', '../task_running', 'test_case.py')
router = Router(tags=["tasks_router"])

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
    task.status = 1
    task.save()
    run2(task_id)
    return response()

@router.get("/{taks_id}",auth=None)
def get_task(request,task_id:int):
    '''
    创建任务
    '''
    task = get_object_or_404(TestTask,id=task_id)
    if task.is_delete is True:
        return  response(error=Error.TASK_DELETE_ERROR)
    relevance = TaskCaseRelevance.objects.filter(task_id=task.id)
    case_list = []
    for r in relevance:
        case_list.append(r.case_id)
    task_dict = model_to_dict(task)
    task_dict['case'] = case_list
    return  response(result=task_dict)

@router.post("/update/{task_id}", auth=None)
def update_case(request, task_id: int,  data: TaskIn):
    task = get_object_or_404(TestTask,id=task_id)
    task.name = data.name
    task.describe = data.describe
    task. save()

    relevance = TaskCaseRelevance.objects.filter(task_id=task_id)
    relevance.delete()
    cases = []
    for case in data.case:
        try:
            TaskCaseRelevance.objects.create(task_id=task.id,case_id=case)
        except IntegrityError:
            return response(error=Error.CASE_DELETE_ERROR)
        case = TestCase.objects.get(pk=case)
        cases.append({
        "case" : case.id,
        "module": case.module_id
        })
    task_dict = model_to_dict(task)
    task_dict["cases"] = cases
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