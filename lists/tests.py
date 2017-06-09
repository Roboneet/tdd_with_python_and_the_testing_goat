from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

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

class ListAndItemModelsTest(TestCase):
	def test_saving_and_retriving_items(self):
		list_ = List()
		list_.save()

		first = Item()
		first.text = 'The first item'
		first.list = list_
		first.save()

		second = Item()
		second.text = 'Item 2'
		second.list = list_
		second.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list,list_)

		all_items = Item.objects.all()
		self.assertEqual(all_items.count(),2)

		first_item = all_items[0]
		second_item = all_items[1]
		self.assertEqual(first_item.text, 'The first item')
		self.assertEqual(first_item.list, list_)
		
		self.assertEqual(second_item.text, 'Item 2')
		self.assertEqual(second_item.list, list_)



class ListTestView(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
    	other_list = List.objects.create()
    	correct_list = List.objects.create()
    	response = self.client.get('/lists/%d/'%(correct_list.id,))
    	self.assertEqual(response.context['list'],correct_list)


class NewListTest(TestCase):
	def test_saving_a_POST_request_to_an_existing_request(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post('/lists/%d/add_item'%(correct_list.id,),data={'item_text': 'A new item for an existing list'})

		self.assertEqual(Item.objects.count(),1)
		new_item = Item.objects.first()
		self.assertEqual('A new item for an existing list', new_item.text)
		self.assertEqual(new_item.list, correct_list)
		

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/lists/%d/add_item'%(correct_list.id,),
			data={'item_text':'A new item for an existing list'}
			)

		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
		
