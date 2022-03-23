# from django.test import TestCase
# from  polls.models import Question,Choice
# from django.utils import timezone
#
#
# # from django.test import Client
# # Create your tests here.
# #用来写测试用例
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
