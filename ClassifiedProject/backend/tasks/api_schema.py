from ninja import Schema
from typing import  List,Any

class TaskIn(Schema):
    '''任务入参'''
    projcet:int
    name: str
    describe: str
    case: list



