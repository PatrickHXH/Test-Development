from django.shortcuts import render
from django.http import  HttpResponse

# Create your views here.
#页面  --> 处理层 -->  数据库里面的数据
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")