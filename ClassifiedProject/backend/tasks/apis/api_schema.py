from ninja import Schema
from typing import  List,Any

class TaskIn(Schema):
    '''任务入参'''
    project:int
    name: str
    describe: str
    cases: list

class ResultOut(Schema):
    id:int
    name: str
    passed: int
    error: int
    failure: int
    skipped: int
    tests: int
    run_time:Any
    # run_time: float
    result: Any
    create_time: Any


class TaskOut(Schema):
    id:int
    name:str
    status:int
    describe: str=None
    create_time: Any
    update_time:Any

class TaskCaseRelevance(Schema):
    id:int
    case:str

class ProjectIn(Schema):
    project_id: int

class CaseLIstIn(Schema):
    caseList: list