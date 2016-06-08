import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

USER_EMAIL = os.environ.get('SMART_DRIVER_USER_EMAIL')
USER_PASSWORD = os.environ.get('SMART_DRIVER_USER_PASSWORD')
USER_NAME = os.environ.get('SMART_DRIVER_USER_NAME')


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def test_can_connect_to_api(self):
        self.browser.get('http://127.0.0.1:8000')
        self.assertIn('Smart Driver', self.browser.title)

    def test_home_page_login_and_test_creation(self):
        self.browser.get('http://127.0.0.1:8000')

        email = self.browser.find_element_by_name('email')
        email.send_keys(USER_EMAIL)

        password = self.browser.find_element_by_name('password')
        password.send_keys(USER_PASSWORD)

        # log-in
        password.send_keys(Keys.ENTER)

        self.browser.implicitly_wait(10)

        # test if
        self.assertIn(USER_NAME, self.browser.page_source)

        self.assertTrue(self.browser.find_element_by_id('table_id'))


if __name__ == '__main__':
    unittest.main()
