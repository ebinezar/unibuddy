import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Initializer(object):
	"""
		Load and parse json file data
	"""
	def __init__(self):
		"""open file in binary format to avoid the encode exception"""
		self._reader = open(os.path.join(BASE_DIR, 'data.json'), 'rb')
		self._parse_data = None

	def fetch_data(self):
		"""parse binary text into dict format"""
		if self._parse_data is None:
			self._parse_data = json.loads(self._reader.read())
			
		return self._parse_data
		
	def __del__(self):
		"""close file before the job completed"""
		self._reader.close()

"""Initialize the loader"""
JsonDB = Initializer()
