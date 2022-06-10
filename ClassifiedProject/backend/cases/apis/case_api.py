from ninja import Router, Query,Path
from django.forms.models import model_to_dict  #将数据库对象转为字典
from backend.common import response,Error  #导入自定义返回
from  cases.models import Module  #导入数据库
from  cases.models import TestCase  #导入数据库
from cases.apis.api_schema import ModuleIn,ProjectIn,CaseIn,CaseDebugIn,CaseAssertIn,CaseOut,ModuleSchema  #导入传参类
from django.shortcuts import get_object_or_404
import requests
from backend.pagination import CustomPagination   #自定义分页
from ninja.pagination import paginate,PageNumberPagination  #分页
from typing import List  #分页用到的列表
import json

router = Router(tags=["cases"])

#创建用例接口
@router.post("/",auth=None)
def create_case(request,data:CaseIn):
    module = Module.objects.filter(id=data.module_id)
    if len(module) == 0:
        return response(error=Error.MODULE_NOT_EXIST)
    else:
        case = TestCase.objects.create(**data.dict())
        return response(result=model_to_dict(case))

#调式接口
@router.post("/debug",auth=None)
def debug_case(request,data:CaseDebugIn):
    url = data.url
    method = data.method
    header = data.header
    params_type = data.params_type
    params_body = data.params_body

    print(type(header),header)
    print(type(params_body), params_body)
    # if method not in  ["get","post"]:
    #     return response(error=Error.CASE_METHOD_ERROR)
    if url == None or url == "":
        return response(error=Error.CASE_URL_ERROR)

    if method == "get":
        resp = requests.get(url,params=params_body,headers=header)
    if method == "post":
        if params_type == "json":
            resp = requests.post(url,json=params_body,headers=header)
        elif params_type == "form":
            resp = requests.post(url,data=params_body,headers=header)
        else:
            return response(error=Error.MODULE_NOT_EXIST)
    print(resp)
    return response(result=resp.text)

#断言接口
@router.post("/assert", auth=None)
def assert_case(request, data: CaseAssertIn):
    """
    用例断言
    auth=None 该接口不需要认证
    """
    print("data", data)
    resp = data.response
    assert_type = data.assert_type
    assert_text = data.assert_text

    # if assert_type not in ["include", "equal"]:
    #     return response(error=Error.CASE_ASSERT_ERROR)

    if assert_type == "include":
        if assert_text in resp:
            return response()
        else:
            return response(success=False)
    elif assert_type == "equal":
        if assert_text == resp:
            return response()
        else:
            return response(success=False)

    return response()

#用例更新接口
@router.post("/update/{case_id}", auth=None)
def update_case(request, case_id: int,  payload: CaseIn):
    """
    更新用例
    auth=None 该接口不需要认证
    """
    case = get_object_or_404(TestCase, id=case_id)
    print(payload.dict().items())
    for attr, value in payload.dict().items():
        setattr(case, attr, value)
    case.save()

    return response()

#删除用例接口
@router.post("/delete/{case_id}", auth=None)
def delete_case(request, case_id: int):
    """
    删除用例
    auth=None 该接口不需要认证
    """
    case = get_object_or_404(TestCase, id=case_id)
    case.is_delete = True
    case.save()

    return response()

#获取用例详情接口
@router.get("/{case_id}/", auth=None)
def case_detail(request, case_id: int):
    """
    获取用例详情
    auth=None 该接口不需要认证
    """
    case = get_object_or_404(TestCase, id=case_id)
    if case.is_delete is True:
        return response(error=Error.CASE_DELETE_ERROR)
    data = {
                "id": case.id,
                "name": case.name,
                "url": case.url,
                "method": case.method,
                "header":case.header,
                "params_type":case.params_type ,
                "params_body": case.params_body,
                "response": case.response,
                "assert_type": case.assert_type ,
                "assert_text":case.assert_text,
                "is_delete": case.is_delete,
                 "create_time": case.create_time,
                "update_time": case.update_time
                }
    return response(result=data)


