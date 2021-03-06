from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
# module 对应的数据库ORM
#python语言  ---> 数据库驱动 --->SQLite3 (sql语言)
#ORM  把写SQL语句给我们屏蔽掉，可以像操作类方法一样操作数据库
#首先，需要按照ORM的方式定义表

# class Persons(models.Model):
#     id = models.IntegerField()
#     LastName = models.CharField(max_length=255)
#     FirstName = models.CharField(max_length=255)
#     Address =models.CharField(max_length=255)
#     City = models.CharField(max_length=255,null=True)

class Question(models.Model):
    question_text = models.CharField(max_length=200)    #定义char类型字段，最大长度为200
    question_desc = models.TextField(null=True,default="")  #定义为非必填，默认为空字符串
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return  self.question_text  #表中数据对象用名称表示

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)      #定义为外键，on_delete必填，models.CASCADE为联级删除
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)              #定义为int字段，默认为0
    def __str__(self):
        return  self.choice_text    #表中数据对象用名称表示


