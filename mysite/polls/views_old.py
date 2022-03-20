from django.shortcuts import render
from django.http import  HttpResponse
from .models import Question,Choice
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
# Create your views here.
#页面  --> 处理层 -->  数据库里面的数据
def index(request):
    print("打印内容 ")
    latest_question_list = Question.objects.order_by('pub_date')[:5]   #取最早5条数据
    context = {'question_list': latest_question_list}
    return  render(request,"polls/index.html",context)

    # output = ', '.join([q.question_text for q in latest_question_list])    #拼接成字符串
    # output = ""
    # for q in latest_question_list:
    #     output = output + q.question_text + ","
    # print(output)
    # return HttpResponse(output)     #返回给前端

def detail(request, question_id):
    '''问题的详情页面'''
    # #第一种获取问题选项的方法
    # all = q.choice_set.all()
    # for i in all:
    #     print(i)
    # #第二种获取问题选项的方法
    # c = Choice.objects.filter(question_id=q.id)
    # for i in c:
    #     print(i)
    '''抛出异常方法1'''
    # try:
    #     q = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise  Http404("Question does not exist")
    # return  render(request,"polls/detail.html",{"question":q})
    '''抛出异常方法2'''
    q = get_object_or_404(Question,id = question_id)
    return render(request, "polls/detail.html", {"question": q})

def results(request, question_id):
    '''投票的结果页面 '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    '''计算投票动作 '''
    q = get_object_or_404(Question,id=question_id)
    try:
        selected_choice = q.choice_set.get(id=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': q,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results',args=(q.id,)))  #args后要逗号

