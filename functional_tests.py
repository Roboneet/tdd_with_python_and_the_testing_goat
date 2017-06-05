from selenium import webdriver
import unittest

# chrome_path = r"/Users/joyp.isahac/Downloads/chromedriver"

# browser = webdriver.Chrome(chrome_path)

# browser.get('http://localhost:8000')
# assert 'To-Do' in browser.title, "Browser Title was "+browser.title

# browser.quit()

class  MyTests(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome(chrome_path)
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_to_start_a_list_and_retrive_it_later(self):

		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do', self.browser.title)
		self.fail("Finish Test")

		self.browser.quit()


if __name__ == '__main__':
	unittest.main(warnings='ignore')