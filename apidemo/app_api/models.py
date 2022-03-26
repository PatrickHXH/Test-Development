from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True,on_delete=models.CASCADE)

# class Department(models.Model):
#     '''部门表'''
#     title = models.CharField(max_length=100)
#
# class Employee(models.Model):
#     '''雇员表'''
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     department = models.ForeignKey(Department,on_delete=models.CASCADE)
#     birthdate = models.DateField(null=True, blank=True)