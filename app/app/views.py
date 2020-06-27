
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.views.generic import View
from django.http import JsonResponse
from search_engine.search import Search

class Books(View):

	"""
	Books find api to query and return the list of result
	"""
	REQUIRED_FIELDS = {'query', 'K'}
	MS_API_URL = 'https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding'
	
	
	@staticmethod
	def update_ms_response(result, api_url):
		for row in result:
			try:
				api_response = requests.post(api_url, json={'book_id':row['id']}, timeout=1)
				print(api_response.json())
				row.update(api_response.json())
			except requests.exceptions.RequestException:
				pass


	def post(self, request):
		"""Post api
			Params
				query : List()
				K	: int()
		"""
		try:
			data = json.loads(request.body.decode('utf-8'))
		except json.decoder.JSONDecodeError:
			return JsonResponse({'message':'API will accept only application/json format'}, status=400)
		
		## validating the the required arguments
		if not self.REQUIRED_FIELDS.issubset(data):
			return JsonResponse({'message':'required fields are missing'}, status=400)

		queries = data['query']
		K = data['K']
		output = []
		threads = []

		for query in queries:
			result = Search.execute(query, K)

			with ThreadPoolExecutor(max_workers=20) as executor:
				threads.append(executor.submit(self.update_ms_response, result, self.MS_API_URL))

			for task in as_completed(threads):
				task.result()
			
			output.append(result)

		return JsonResponse({'output': output})
			