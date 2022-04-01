from ninja import Router,File
from django.forms.models import model_to_dict
from backend.common import response,Error
from  cases.models import Module
from  cases.api_schema import ModuleIn

router = Router(tags=["cases"])

#创建模块s
@router.post("/create/",auth=None)
def create_module(request,data:ModuleIn):
    project = Project.objects.filter(id=data.project_id)
    if len(project) == 0:
        return response(error=Error.PROJECT_NOT_EXIST)
    module = Module.objects.filter(name=data.name,project_id=data.project_id)
    if len(module) > 0:
        return response(error=Error.MODULE_NAME_EXIST)
    else:
        module = Module.objects.create(**data.dict())
        return  response(result=model_to_dict(module))