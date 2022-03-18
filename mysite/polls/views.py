from django.shortcuts import render
from django.http import  HttpResponse
from .models import Question

# Create your views here.
#页面  --> 处理层 -->  数据库里面的数据
def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]   #取最早5条数据
    output = ', '.join([q.question_text for q in latest_question_list])    #拼接成字符串
    # output = ""
    # for q in latest_question_list:
    #     output = output + q.question_text + ","
    return HttpResponse(output)     #返回给前端

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)