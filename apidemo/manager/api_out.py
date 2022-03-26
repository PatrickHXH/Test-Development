from ninja import Router,Schema
from .models import Department,Employee
from datetime import date

class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None