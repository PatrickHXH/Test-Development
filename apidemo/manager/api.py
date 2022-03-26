from ninja import Router,Schema
from .models import Department,Employee
from datetime import date
from manager.api_in import EmployeeIn,DepartmentIn
from manager.api_out import EmployeeOut
from django.shortcuts import get_object_or_404
from typing import List

router = Router(tags=["manager"])

'''
**payload.dict() 当入参字段与数据库字段一致时可以使用这种写法
格式等同于如下：
 employee = Employee.objects.create(
    id  = payload.id
 )
'''
#创建部门
@router.post("/department")
def create_department(request, payload: DepartmentIn):
    department = Department.objects.create(**payload.dict())
    return {"id": department.id}


#创建员工
@router.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}

#根据雇员的id查询
@router.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee

#查询雇员所有数据
@router.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs

#更新雇员数据
@router.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    print(payload.dict().items())
    '''
    打印格式：
    dict_items([('first_name', 'string'), ('last_name', 'string'), ('department_id', 1), ('birthdate', datetime.date(2022, 3, 26))])
    '''
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}

#删除雇员
@router.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}