
from search_engine import JsonDB

class Search():
	"""
	Search engine to query words from the loaded data
	"""

	search_record_key = 'summary'

	@staticmethod
	def indexing(data, field):
		"""index search data in generator for quick access"""
		return (record[field].lower() for record in data)

	@staticmethod
	def find_words(data_list, query):
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

	@classmethod
	def execute(cls, query, K):
		"""main method to find and return relavant matches"""

		query = query.lower()

		data = JsonDB.fetch_data()
		summaries = data['summaries']

		data_list = cls.indexing(summaries, cls.search_record_key)

		relevant_indexes = sorted(cls.find_words(data_list, query), reverse=True)
		
		return [summaries[index] for _, index in relevant_indexes[:K]]
