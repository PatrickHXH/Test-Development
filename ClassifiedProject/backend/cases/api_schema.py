from ninja import Schema
from typing import  List,Any

class ModuleIn(Schema):
    name: str
    project_id: int
    parent_id: int=0


class ProjectOut(Schema):
    id:int
    name: str
    describe: str
    image: str=None
    create_time: Any
    update_time: Any