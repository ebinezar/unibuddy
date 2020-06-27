from django.test import TestCase
from django.urls import reverse


class BooksTestCase(TestCase):
	"""
	Test cases to test book finding api
	"""
	def setUp(self):
		self.api_name = 'books_find'
		self.invalid_query = ["Lorem Ipsum", "Lorem Ipsum"]
		self.valid_query = ["is your problems", "achievetake book"]
		self.K = 4

	def post_request(self, data):
		response = self.client.post(reverse(self.api_name), data=data, content_type="application/json")
		self.assertEqual(response.status_code, 200)
		return response.json()

	def test_find_with_invalid_query(self):
		"""Find books with invalid query"""
		data = {
			'query': self.invalid_query,
			'K': self.K
		}
		response_json = self.post_request(data)

		self.assertIn('output', response_json)
		for result in response_json['output']:
			self.assertListEqual(result, list())

	def test_find_with_valid_query(self):
		"""Find books with valid query"""
		data = {
			'query': self.valid_query,
			'K': self.K
		}
		response_json = self.post_request(data)

		self.assertIn('output', response_json)
		for result in response_json['output']:
			self.assertLessEqual(len(result), self.K)
	