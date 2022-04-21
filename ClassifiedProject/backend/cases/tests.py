from django.test import TestCase

# Create your tests here.
{
"url": "http://httpbin.org/get",
"method": "post",
"header" :{"totken": "123"},
"params_type":"params",
"params_body": {"hello" : "wrold"}
}
def hello_3(x='Hello',y='world'):#定义函数
    print('%s,%s!'%(x,y))

params={'x':'Sir Robin','y':'Well met'}

hello_3(**params)#调用,参数为**params