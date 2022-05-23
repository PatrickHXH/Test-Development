import hashlib

from ninja import Router,File
from django.forms.models import model_to_dict
from backend.common import response,Error
from backend.pagination import CustomPagination
from ninja.pagination import paginate,PageNumberPagination  #分页
from typing import List
from projects.api_schema import ProjectIn,ProjectOut
from projects.models import Project
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from ninja.files import UploadedFile
import os
from  backend.settings import IMAGE_DIR
router = Router(tags=["projects"])

#创建项目接口
@router.post("/create",auth=None)
def create_project(request,data:ProjectIn):
    name = data.name
    describe = data.describe
    image = data.image

    project = Project.objects.filter(name=name)
    if len(project) > 0:
        return  response(error=Error.PROJECT_NAME_EXIST)
    else:
        Project.objects.create(**data.dict())
        return  response()

#项目列表接口
@router.get("/list",auth=None,response=List[ProjectOut])  #自定义分页必须加response
@paginate(CustomPagination)
def project_list(request):
    projects = Project.objects.filter(is_delete=False).all()
    return projects

#获取详情接口
@router.get("/{project_id}",auth=None)
def project_detail(request,project_id:int):
    # try:
    #     project = Project.objects.get(id=project_id)
    # except project.DoesNotExist:
    #     return response(error=Error.PROJECT_NAME_EXIST)
    # else:
    project = get_object_or_404(Project,id=project_id)
    if project.is_delete is True:
        return  response(error=Error.PROJECT_IS_DELETE)
    else:
        data = {
            "id": project.id,
            "name": project.name,
            "describe": project.describe,
            "image": project.image,
            "create_time":project.create_time
            }
    return  response(result=data)

#更新项目接口
@router.put("/{project_id}",auth=None)
def project_update(request,project_id:int,data:ProjectIn):
    project = get_object_or_404(Project,id=project_id)
    for atr,value in data.dict().items():
        setattr(project,atr,value)
    project.save()
    '''
        Project.objects.filter(id=project_id).update(image=data.image, name=data.describe,describe=data.describe)

    '''
    return response()

#删除项目接口
@router.delete("/{project_id}",auth=None)
def project_delete(request,project_id:int):
    project = get_object_or_404(Project,id=project_id)
    project.is_delete = True
    project.save()
    return response()

#图片上传接口

@router.post("/upload/",auth=None)
def upload(request, file: UploadedFile = File(...)):
    # data = file.read()
    # print(file.name)
    # print(file.size)
    file_type = ["png", "jpg", "jpeg", "txt"]
    type = file.name.split(".")[-1]
    if type not in file_type:
        return  response(error=Error.FLIE_TYPE_ERROR)
    else:
        #文件名生成MD5
        file_md5 = hashlib.md5(bytes(file.name,encoding="utf-8")).hexdigest()
        file_name = file_md5+"."+type
        # file_dir = os.path.dirname(os.path.abspath(__file__))
        print("重命名图片：",file_name)
        upload_file= os.path.join(IMAGE_DIR,file_name)
        print(upload_file)
        with open(upload_file,"wb+") as f:
            for chunk in file.chunks():   #file.chunks()类似与file.read()
                f.write(chunk)
        return response(result={"name":file_name})