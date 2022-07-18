from ninja import Schema
from typing import  List,Any
from enum import Enum

class ProjectIn(Schema):
    project_id: int

class ModuleIn(Schema):
    name: str
    project_id: int
    parent_id: int=0


class Method(str, Enum):
    """请求方法"""
    get = "get"
    post = "post"


class ParamsType(str, Enum):
    """参数类型"""
    params = "params"
    form = "form"
    json = "json"


class AssertType(str, Enum):
    """断言类型"""
    include = "include"
    equal = "equal"

class CaseIn(Schema):
    module_id: str
    name:str
    url:str
    method:Method
    header:dict
    params_type:ParamsType
    params_body:dict
    response:str
    assert_type:AssertType
    assert_text:str
    extract_list: list = None


class CaseDebugIn(Schema):
    url:str
    method:Method
    header:dict
    params_type:ParamsType
    params_body:dict

class CaseAssertIn(Schema):
    response:str
    assert_type:AssertType
    assert_text:str



#获取用例列表所用的传参
class ModuleSchema(Schema):
    id: int
    name: str

class CaseOut(Schema):
    id:int
    name: str
    module_id: int
    url: str
    method: str
    module: ModuleSchema = None  # 关联外键表模块
    create_time: Any
    update_time: Any

class checkExtractIn(Schema):
    response:str
    extractList:list

class ExtractOut(Schema):
    id:int
    name: str
    extract: str
    vlue: str
    case_id: str
    create_time: Any
    update_time:Any