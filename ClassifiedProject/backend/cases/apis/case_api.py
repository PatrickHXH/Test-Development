from ninja import Router, Query,Path
from django.forms.models import model_to_dict  #将数据库对象转为字典
from backend.common import response,Error  #导入自定义返回
from  cases.models import TestCase,TestExtract,Module #导入数据库
from cases.apis.api_schema import ModuleIn,ProjectIn,CaseIn,CaseDebugIn,CaseAssertIn,CaseOut,ModuleSchema,checkExtractIn  #导入传参类
from django.shortcuts import get_object_or_404
import requests
from backend.pagination import CustomPagination   #自定义分页
from ninja.pagination import paginate,PageNumberPagination  #分页
from typing import List  #分页用到的列表
import json
import jmespath
from  cases.apis.common import  get_replace_string
import sqlite3
router = Router(tags=["cases"])

#创建用例接口
@router.post("/",auth=None)
def create_case(request,data:CaseIn):
    # module = Module.objects.filter(id=data.module_id)
    # if len(module) == 0:
    #     return response(error=Error.MODULE_NOT_EXIST)
    # else:
    #     print(data.dict())
    #     case = TestCase.objects.create(**data.dict())
    #     return response(result=model_to_dict(case))
    print(data)
    module = get_object_or_404(Module,id=data.module_id)
    case = TestCase.objects.create(
        name=data.name,
        module_id=data.module_id,
        url=data.url,
        method=data.method,
        header=data.header,
        params_type=data.params_type,
        params_body=data.params_body,
        response=data.response,
        assert_type=data.assert_type,
        assert_text=data.assert_text
    )
    print("打印")
    for extract in data.extract_list:
        if extract["name"] == "" or extract["value"] == "":
            continue
        extract_obj = TestExtract.objects.filter(project_id=module.project_id,name=extract["name"])
        if len(extract_obj) > 0:
            extract_obj.extract = extract["value"]
        else:
            print(case.id)
            TestExtract.objects.create(
                project_id=module.project_id,
                case_id=case.id,
                name=extract["name"],
                extract=extract["value"]
            )
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

    url = get_replace_string(url)
    print(url)

    header_new = {}
    for key,value in header.items():
        header_new[key] = get_replace_string(value)
    print("header_new",header_new)

    params_body_new = {}
    for key,value in params_body.items():
        params_body_new[key] = get_replace_string(value)
    print("params_body_new",params_body_new)

    # if method not in  ["get","post"]:
    #     return response(error=Error.CASE_METHOD_ERROR)
    if url == None or url == "":
        return response(error=Error.CASE_URL_ERROR)

    if method == "get":
        resp = requests.get(url,params=params_body_new,headers=header_new)
    if method == "post":
        if params_type == "json":
            resp = requests.post(url,json=params_body_new,headers=header_new)
        elif params_type == "form":
            resp = requests.post(url,data=params_body_new,headers=header_new)
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

    module = get_object_or_404(Module, id=payload.module_id)
    for extract in payload.extract_list:
        if extract["name"] == "" or extract["value"] == "":
            continue
        extract_obj = TestExtract.objects.filter(
            project_id=module.project_id, name=extract["name"])
        if len(extract_obj) > 0:
            extract_obj.extract = extract["value"]
        else:
            TestExtract.objects.create(
                project_id=module.project_id,
                case_id=case.id,
                name=extract["name"],
                extract=extract["value"]
            )
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

#检查提取器
@router.post("/extract", auth=None)
def chect_extract(request, data: checkExtractIn):
    try:
        resp = json.loads(data.response)
    except json.decoder.JSONDecodeError:
        return response(error=Error.CHECK_RESP_ERROR)
    extract_list = data.extractList
    print(resp)
    for extract in extract_list:
        extract_value = extract["value"]
        extract_name = extract["name"]
        if extract_value == "" or  resp == "" or extract_name == "":
            return response(error=Error.CHECK_EXTRACT_NULL_ERROR)
        try:
            result = jmespath.search(extract_value,resp)
            print(result)
            if result is None:
                return response(error={"10057":f"提取器错误:{extract_value}"})
        except jmespath.exceptions.ParseError:
            return response(error=Error.CHECK_EXTRACT_ERROR)
    return  response()