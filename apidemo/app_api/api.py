from ninja import NinjaAPI,Form,Router
from ninja import Schema, Path
import  datetime
from django.contrib.auth.models import User

router= Router(tags=["app_api"])

@router.get("/add")
def add(request,a:int,b:int,c:int):
    return  {"resutlt": a+b}
#相同接口多种方法
@router.api_operation(["GET","POST","DELETE"],"/user/{user_id}/")
def user(request,user_id:int):
    if request.method == "GET":
        return  {"result":"get user info"}
    if request.method == "DELETE":
        return  {"result":"DELETE user info"}
@router.get("/items/{item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}

#使用get传递类方法传参，需要加Path(...)
class PathDate(Schema):
    year: int
    month: int
    day: int
    def value(self):
        return datetime.date(self.year, self.month,self.day)
@router.get("events/{year}/{month}/{day}")
def events(request,date:PathDate=Path(...)):
    return {"date":date.value()}

#GET在URL中传参,格式api/xx&xx
weapons = ["Ninjato", "Shuriken", "Katana", "Kama", "Kunai", "Naginata", "Yari"]
@router.get("/weapons")
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
@router.get("/filter")
def events(request, filters: Filters = Query(...)):
    return {"filters": filters.dict()}

#post传参  创建+更新
class Item(Schema):
    name: str
    description: str = None
    price: float
    quantity: int
@router.post("/items")
def create(request, item: Item):
    return item
@router.post("/items/{item_id}")
def update(request,item_id:int, item: Item):
    return {"item_id": item_id, "item": item.dict()}

#form-data格式传参，可以上传文件
from ninja import NinjaAPI,Form
@router.post("login")
def login(request,username:str = Form(...),passwd:str = Form(...)):
    return {"username":username,'password':'*********'}

#文件上传传参
'''
文件上传：
1、post方法 + form-data格式
2、名称，大小
3、上传文件保存！！新建一个文件，把上传的文件内容读出来，写到新建文件
        上传的文件属性和方法和django中相同，主要包括以下：
        read()
        从文件中读取整个上传的文件。文件太大会报错。
        multiple_chunks(chunk_size=None)
        如果上传的文件足够大，需要分块读取，返回True。默认情况下是大于2.5M的文件。
        chunks(chunk_size=None)
        一个生成器，返回文件的块。
        name
        上传文件的文件名
        size
        上传文件的大小，以字节为单位
        content_type
        与文件一起上传的内容类型头
        content_type_extra
        包含传递给content-type头的额外参数的字典。
        charset
        对于text/*内容类型，浏览器提供的字符集。
'''
file_type = ["png","jpg","jpeg","txt"]
import os
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
@router.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    # print(file.name)
    # print(file.size)
    type = file.name.split(".")[-1]
    if type not in file_type:
        return {"error":"不支持该文件类型上传"}
    else:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        upload_file= os.path.join(file_dir,"upload",file.name)
        local_file =open(upload_file,"wb")
        for chunk in file.chunks():
            local_file.write(chunk)
        local_file.close()
        return {'name': file.name, 'len': len(data)}

#使用response自定义返回数据
from ninja import Schema
class UserIn(Schema):
    username: str
    password: str
class UserOut(Schema):
    id:int
    username:str
    password:str
@router.post("/users/",response=UserOut)
def create_user(request,data:UserIn):
    user = User(username=data.username)
    user.set_password(data.password)
    user.save()
    return user

#关联数据库返回
from typing import List,Optional
from ninja import Schema
from .models import  Task
from ninja import Field, Schema
class UserSchema(Schema):
    id: int
    first_name: str
    last_name: str
    password:str
    username:str
class TaskSchema(Schema):
    id: int
    title: str
    is_completed: bool
    owner: UserSchema = None  # ! None - to mark it as optional
class TaskSchema(Schema):      #返回字段与数据库定义不一致
    id: int
    title: str
    completed: bool = Field(..., alias="is_completed")
    owner_user_name: str = Field(None, alias="owner.username")
# class TaskSchema(Schema):    #返回中定义方法
#     id: int
#     title: str
#     is_completed: bool
#     owner: Optional[str]
#     lower_title: str
#     @staticmethod
#     def resolve_owner(obj):
#         if not obj.owner:
#             return
#         else:
#             return f"{obj.owner.first_name} {obj.owner.last_name}"
#     def resolve_lower_title(self,obj):
#         return self.title.lower()
@router.get("/tasks", response=List[TaskSchema])
def tasks(request):
    queryset = Task.objects.select_related("owner")   #select_related()函数后，Django会获取相应外键对应的对象，从而在之后需要的时候不必再查询数据库了
    return list(queryset)


#自定义返回状态码
class Token(Schema):
    token: str
class Message(Schema):
    message: str
class Auth(Schema):
    token: str
@router.post('/login2', response={200: Token, 401: Message, 402: Message})
def login2(request, payload: Auth):
    if payload.token == 1:
        return 401, {'message': 'Unauthorized'}
    if payload.token == 2:
        return 402, {'message': 'Insufficient balance amount. Please proceed to a payment page.'}
    return 200, {'token': payload.token}

