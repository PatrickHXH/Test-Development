from django.test import TestCase
from  polls.models import Question,Choice
from django.utils import timezone
from selenium.webdriver.chrome.webdriver import WebDriver

# from django.test import Client
# Create your tests here.
#用来写测试用例
# model测试
# class StudyTestCsse(TestCase):
#     def setUp(self):
#         Question.objects.create(id=1,question_text="你的女朋友是谁?",pub_date=timezone.now())
#
#     def test_01(self):
#         u'''测试查询问题'''
#         question = Question.objects.get(id=1)
#         self.assertIn("你的女朋友是谁?",question.question_text)
#
#     def test_02(self):
#         u'''测试创建问题'''
#         Question.objects.create(id=2,question_text="今天吃什么?",pub_date=timezone.now())
#         question = Question.objects.get(id=2)
#         self.assertIn("今天吃什么",question.question_text)
#
#     def test_03(self):
#         u'''测试更新数据'''
#         question = Question.objects.get(id=1)
#         Question.objects.filter(id=1).update(question_text="周末是否加班")
#         question = Question.objects.get(id=1)
#         self.assertIn("周末是否加班",question.question_text)
#
#     def test_04(self):
#         u'''测试删除数据'''
#         question = Question.objects.get(id=1)
#         Question.objects.filter(id=1).delete()
#         self.assertEqual(0,len(Question.objects.all()))
#
# class choiceTestcase(TestCase):
#
#     def setUp(self):
#         Question.objects.create(id=1,question_text="what's new?",pub_date=timezone.now())
#         Choice.objects.create(id=1,choice_text='Not Much',votes=0,question_id=1)
#         Choice.objects.create(id=2,choice_text='The sky',votes=0,question_id=1)
#
#     def test_choice_query(self):
#         u'''测试问题选项查询'''
#         choice = Choice.objects.get(id=1)
#         self.assertEqual(choice.choice_text,"Not Much")
#
# #client测试
# class IndexTestCase(TestCase):
#     def setUp(self):
#         Question.objects.create(id=1, question_text="what is new?", pub_date=timezone.now())
#         Choice.objects.create(id=1,choice_text='Not Much',votes=0,question_id=1)
#         Choice.objects.create(id=2,choice_text='The sky',votes=777,question_id=1)
#
#     def test_index_page(self):
#         u'''测试问题列表'''
#         response = self.client.get("/polls/")
#         # self.assertEqual(200,response.status_code)
#         self.assertIn(b"what is new",response.content)
#         self.assertTemplateUsed(response,"polls/index.html")
#
#     def test_detail_page(self):
#         u'''测试问题详情页'''
#         response = self.client.get("/polls/1/")
#         self.assertEqual(200, response.status_code)
#         self.assertIn(b"Not Much", response.content)
#         self.assertIn(b"The sky", response.content)
#
#     def test_result_page(self):
#         u'''测试投票结果页'''
#         response = self.client.get("/polls/1/results/")
#         print(response.content)
#         self.assertEqual(200, response.status_code)
#         self.assertIn(b"777", response.content)
#
#     def test_vote_action(self):
#         u'''测试投票动作'''
#         response = self.client.post("/polls/1/vote/",data = {"choice":2})
#         print(response.content)
#         self.assertEqual(302, response.status_code)
#         response = self.client.get("/polls/1/results/")
#         self.assertIn(b"778", response.content)
