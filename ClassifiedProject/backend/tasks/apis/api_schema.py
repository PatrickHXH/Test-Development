from ninja import Schema
from typing import  List,Any

class TaskIn(Schema):
    '''任务入参'''
    projcet:int
    name: str
    describe: str
    case: list

class ResultOut(Schema):
    name: str
    passed: int
    error: int
    failure: int
    skipped: int
    tests: int
    # run_time: float
    # result: int
    # create_time: Any


