from django.contrib import admin

# Register your models here.
#django自带一个admin后台
from  .models import  Question ,Choice

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text','pub_date','question_desc']         #显示表中字段
    search_fields = ['question_text ']                                                #显示搜索内容
admin.site.register(Question,QuestionAdmin)                              #显示表、点击显示表中字段和内容

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text','votes','question']
admin.site.register(Choice,ChoiceAdmin)