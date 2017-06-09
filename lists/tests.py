from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):
	def test_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func,home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(),expected_html)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method='POST'
		request.POST['item_text'] = 'A new list item'
		response = home_page(request)

		self.assertEqual(Item.objects.count(),1)
		first_item = Item.objects.first()
		self.assertEqual('A new list item', first_item.text)

		self.assertIn('A new list item', response.content.decode())
		expected_html = render_to_string('home.html',{'new_item_text': 'A new list item'})
		self.assertEqual(response.content.decode(),expected_html)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'],'/')

	def test_home_page_only_saves_items_when_neseccary(self):
		request = HttpRequest()
		response = home_page(request)
		self.assertEqual(Item.objects.count(),0)


class ItemModelTest(TestCase):
	def test_saving_and_retriving_items(self):
		first = Item()
		first.text = 'The first item'
		first.save()

		second = Item()
		second.text = 'Item 2'
		second.save()

		all_items = Item.objects.all()
		self.assertEqual(all_items.count(),2)

		first_item = all_items[0]
		second_item = all_items[1]
		self.assertEqual(first_item.text, 'The first item')
		self.assertEqual(second_item.text, 'Item 2')
