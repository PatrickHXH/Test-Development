from django.db import models

# Create your models here.
# module 对应的数据库ORM
#python语言  ---> 数据库驱动 --->SQLite3 (sql语言)
#ORM  把写SQL语句给我们屏蔽掉，可以像操作类方法一样操作数据库

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)