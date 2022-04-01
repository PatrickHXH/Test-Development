from ninja import Schema
from typing import  List,Any

class ProjectIn(Schema):
    name: str
    describe: str
    image: str=None


class ProjectOut(Schema):
    id:int
    name: str
    describe: str
    image: str=None
    create_time: Any
    update_time: Any