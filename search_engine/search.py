import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class LoadData(object):
	"""
		Load and parse json file data
	"""
	def __init__(self):
		"""open file in binary format to avoid the encode exception"""
		self._reader = open(os.path.join(BASE_DIR, 'data.json'), 'rb')

	def fetch_data(self):
		"""parse binary text into dict format"""
		return json.loads(self._reader.read())
		
	def __del__(self):
		"""close file before the job completed"""
		self._reader.close()


class Search(LoadData):
	"""
	Search engine to query words from the loaded data
	"""

	search_record_key = 'summary'

	def indexing(self, data, field):
		"""index search data in generator for quick access"""
		return (record[field].lower() for record in data)

	def find_words(self, data_list, query):
		"""iterate indexed data to find relevant match"""
		words = query.split()
		words_len = len(words)

		q_index = 0
		word_count = []
		for i, word in enumerate(words):
			word_count.append((i, q_index))
			q_index += len(word)+1

		index = 0
		for record in data_list:
			for w_index, q_index in word_count:
				if query[q_index:] in record:
					count = words_len - w_index
					yield (count, index)
					break
			index += 1

	def Query(self, query, K):
		"""main method to find and return relavant matches"""

		query = query.lower()

		data = self.fetch_data()
		summaries = data['summaries']

		data_list = self.indexing(summaries, self.search_record_key)

		relevant_indexes = sorted(self.find_words(data_list, query), reverse=True)
		
		return [summaries[index] for _, index in relevant_indexes[:K]]
