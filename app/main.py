from app.csv.utils import CsvReader, CsvWriter
from app.http.services import RestClient
from app.student.utils import Transformer

import logging

logger = logging.getLogger(__name__)


class Application:

	def __init__(self):
		self.url_index = None
		self.urls = [
			'https://node-data-generator.herokuapp.com/api/names/fullNames?n=5000',
			'https://randomuser.me/api/?inc=name&results=5000&nat=us'
		]

	def get_generated_names(self):
		self.url_index = 1 if self.url_index == 0 else 0
		return RestClient.get(self.urls[self.url_index])

	def start(self):
		logger.info('Application has started')
		schools = CsvReader.read()

		logger.info('Read [%s] records', len(schools))
		student_profiles = []
		students = []

		for school in schools:
			logger.info('School: %s', school['Name'])

			for index in range(0, 1000):

				if len(students) == 0:
					data = self.get_generated_names()

					if self.url_index == 1:
						students = data['results']
					else:
						students = data

				student_profiles.append(Transformer.create_student_profile(students.pop(0), school))

		CsvWriter.write(data=student_profiles)
