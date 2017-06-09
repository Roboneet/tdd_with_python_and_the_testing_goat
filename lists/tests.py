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

class ListTestView(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')


	def test_home_page_displays_all_items(self):
		Item.objects.create(text='Why this kolavari di?')
		Item.objects.create(text='I am tItAniUm')

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response,'Why this kolavari di?')
		self.assertContains(response,'I am tItAniUm')


class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post('/lists/new',data={'item_text': 'A new list item'})

		self.assertEqual(Item.objects.count(),1)
		first_item = Item.objects.first()
		self.assertEqual('A new list item', first_item.text)
		

	def test_home_page_redirects_after_a_POST_request(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text':'A new list item'}
			)

		self.assertRedirects(response,'/lists/the-only-list-in-the-world/')
