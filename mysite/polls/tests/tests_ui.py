from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import WebDriver

class MySeleniumTests(StaticLiveServerTestCase):


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        selenium.get("http://127.0.0.1:8000/polls")
        selenium.find_element(By.ID,"1").click()
        selenium.find_element(By.XPATH,"//input[@type='radio' and @ value='1']").click()
        selenium.find_element(By.ID, "voteButton").click()