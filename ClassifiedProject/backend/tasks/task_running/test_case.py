import os
import unittest
import requests
from XTestRunner import XMLTestRunner
from ddt import ddt, data, file_data, idata, unpack

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA = os.path.join(BASE_DIR,'test_data.json')
TEST_REPORT = os.path.join(BASE_DIR, "xml_result.xml")


@ddt
class MyTest(unittest.TestCase):

    @file_data(TEST_DATA)
    def test_api(self, url, method, header, params_type, params_body, assert_type, assert_text):
        resp=""
        if method == "get":
            resp = requests.get(url, params=params_body)

        if method == "post":
            if params_type == "json":
                resp = requests.post(url, json=params_body, headers=header)
            elif params_type == "form":
                resp = requests.post(url, data=params_body, headers=header)

        if assert_type == "include":
            self.assertIn(assert_text,resp.text)

        elif assert_type == "equal":
            self.assertEqual(assert_text,resp.text)

if __name__ == '__main__':
    with (open(TEST_REPORT,"wb")) as fp:
        unittest.main(testRunner=XMLTestRunner(output=fp))