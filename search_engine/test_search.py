import unittest
from search_engine.search import Search

class SearchJsonTest(unittest.TestCase):

	def setUp(self):
		self.valid_query = "is your problems"
		self.invalid_query = "Lorem Ipsum Lorem Ipsum"
		self.records_count = 4
		
	def setup_method(self, method):
		print("\n%s:%s" % (type(self).__name__, method.__name__))

	def test_with_invalid_query(self):
		response = Search.execute(self.invalid_query, self.records_count)
		assert len(response) == 0

	def test_with_valid_query(self):
		response = Search.execute(self.valid_query, self.records_count)
		assert len(response) == self.records_count


if __name__ == '__main__':
	command = 'python -m test_search or pytest -s'
	unittest.main()
	