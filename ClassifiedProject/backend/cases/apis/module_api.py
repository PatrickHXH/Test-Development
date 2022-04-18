from ninja import Router, Query
from django.forms.models import model_to_dict
from backend.common import response,Error
from  cases.models import Module
from cases.apis.api_schema import ModuleIn,ProjectIn,CaseOut
from django.shortcuts import get_object_or_404
from typing import List  #分页用到的列表
from backend.pagination import CustomPagination   #自定义分页
from ninja.pagination import paginate,PageNumberPagination  #分页
from  cases.models import TestCase

router = Router(tags=["modules"])

#创建模块接口
@router.post("/create/",auth=None)
def create_module(request,data:ModuleIn):
    project = Project.objects.filter(id=data.project_id)
    if len(project) == 0:
        return response(error=Error.PROJECT_NOT_EXIST)
    module = Module.objects.filter(name=data.name,project_id=data.project_id)
    if len(module) > 0:
        return response(error=Error.MODULE_NAME_EXIST)
    else:
        module = Module.objects.create(**data.dict())   #传参转为字典创建数据
        return  response(result=model_to_dict(module))  #数据对象转为字典



#递归,将子节点放入父节点
def tree_node(all_nodes,current_node):
    for i in all_nodes:
        if current_node["id"] == i["parent_id"]:
            current_node["children"].append(i)
            tree_node(all_nodes,i)
    return current_node

#判断该节点是否有子节点，用true和False返回
def children_node(all_nodes,current_node):
    for i in all_nodes:
        if current_node["id"] == i["parent_id"]:
            return True
    return False

#获取项目模块接口
@router.get("/tree",auth=None)
def project_module_tree(request,data:ProjectIn=Query(...)):
    modules = Module.objects.filter(project_id = data.project_id,is_delete=False)
    list = []
    for i in modules:
        list.append({"id": i.id,
                            "name":i.name,
                            "parent_id":i.parent_id,
                            "children":[],
                            "create_time":i.create_time
                     })
    data = []
    for i in list:
        #判断该节点是否有子节点，用true和False返回
        is_children = children_node(list,i)
        if (i["parent_id"]==0) and (is_children is False):
            data.append(i)
        elif (i["parent_id"]==0) and (is_children is True):
            ret = tree_node(list,i)
            data.append(ret)
    return response(result=data)

#删除节点接口
@router.get("/delete/{module_id}",auth=None)
def delete_tree(request,module_id:int):
    module = get_object_or_404(Module, id=module_id)
    module.is_delete = True
    module.save()
    return response()

#获取用例列表接口,分页
@router.get("/{module_id}/cases",auth=None,response=List[CaseOut])  #自定义分页必须加response
@paginate(CustomPagination)
def case_list(request,module_id: int,**kwargs):
    cases = TestCase.objects.filter(module_id=module_id, is_delete=False)
    return cases

