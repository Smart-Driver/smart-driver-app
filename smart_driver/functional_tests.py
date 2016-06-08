import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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
        email.send_keys('julio_jr3@hotmail.com')

        password = self.browser.find_element_by_name('password')
        password.send_keys('juliojr77julio7')

        password.send_keys(Keys.ENTER)

        self.browser.implicitly_wait(10)

        # test if user's name is at top of page
        self.assertIn('Julio', self.browser.page_source)

        # test if table loads properly
        self.assertTrue(self.browser.find_element_by_id('table_id'))


if __name__ == '__main__':
    unittest.main()
