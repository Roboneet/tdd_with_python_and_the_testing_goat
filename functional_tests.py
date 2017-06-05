from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
		
		header_txt = self.browser.find_element_by_tag_name('h1').text()
		self.assertIn('To-Do', header_txt)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute(placeholder),'Enter a to-do item')
		inputbox.send_keys('Buy peacock feathers')

		self.browser.send_keys(Keys.RETURN)

		table = self.browser.find_element_by_tag_name('table')
		rows = table.find_elements_by_tag_name('tr')
		slef.assertTrue(
			any(row.text == '1: Buy Peacock feathers' for row in rows)
			)

		self.fail("Finish Test")
		self.browser.quit()


if __name__ == '__main__':
	unittest.main(warnings='ignore')