from django.contrib import admin
from  .models import  Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','title','is_completed','owner']         #显示表中字段

admin.site.register(Task,TaskAdmin)                              #显示表、点击显示表中字段和内容

