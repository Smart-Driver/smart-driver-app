import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)


    # def tearDown(self):
    #     self.browser.quit()


    def test_can_connect_to_api(self):
        self.browser.get('http://127.0.0.1:8000')
        self.assertIn('Smart Driver', self.browser.title)


    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['email'] = 'email address'
        request.POST['password'] = 'password'
        response = home_page(request)
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
