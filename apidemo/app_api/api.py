from ninja import NinjaAPI
from ninja import Schema, Path
import  datetime
api = NinjaAPI( )

@api.get("/add")
def add(request,a:int,b:int,c:int):
    return  {"resutlt": a+b}
@api.api_operation(["GET","POST","DELETE"],"/user/{user_id}/")
def user(request,user_id:int):
    if request.method == "GET":
        return  {"result":"get user info"}
    if request.method == "DELETE":
        return  {"result":"DELETE user info"}
@api.get("/items/{item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}

#使用类方法传参
class PathDate(Schema):
    year: int
    month: int
    day: int
    def value(self):
        return datetime.date(self.year, self.month,self.day)
@api.get("events/{year}/{month}/{day}")
def events(request,date:PathDate=Path(...)):
    return {"date":date.value()}


#GET在URL中传参,格式api/xx&xx
weapons = ["Ninjato", "Shuriken", "Katana", "Kama", "Kunai", "Naginata", "Yari"]
@api.get("/weapons")
def list_weapons(request, limit: int = None, offset: int = 0):
    if limit is None:
        limit = 10
    return weapons[offset: offset + limit]

#返回值带列表
import datetime
from typing import List  #用来定义列表内的类型
from pydantic import Field  #用来添加默认值
from ninja import Query, Schema
class Filters(Schema):
    limit: int = 100
    offset: int = None
    query: str = None
    category__in: List[str] = Field(None, alias="categories")    #Field（非空，别名）
@api.get("/filter")
def events(request, filters: Filters = Query(...)):
    return {"filters": filters.dict()}