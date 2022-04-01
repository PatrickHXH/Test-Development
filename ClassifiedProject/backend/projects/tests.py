from django.test import TestCase
import  requests
# Create your tests here.

for i in range(0,11):
    json = {
        "name" : "测试系统" + str(i),
        "describe":"测试描述" + str(i),
        "img":"123.png"
    }
    requests.post(url="http://127.0.0.1:8000/api/projects/create",json=json)