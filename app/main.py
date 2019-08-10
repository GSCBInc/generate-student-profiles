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
		skipped_students = 0
		students_by_name = {}
		student_profiles = []
		students = []

		# for school in schools:
		while len(schools) > 0:
			index = 0
			duplicates_found = 0
			school = schools.pop(0)
			logger.info('School: %s', school['Name'])
			while index < 1000:

				if len(students) == 0:
					data = self.get_generated_names()

					if self.url_index == 1:
						students = data['results']
					else:
						students = data

				student_profile = Transformer.create_student_profile(students.pop(0), school)

				# Make sure student Name is not a duplicate
				if not students_by_name.__contains__(student_profile['Name']):
					student_profiles.append(student_profile)
					students_by_name[student_profile['Name']] = student_profile
					index += 1
				else:
					logger.info('%s is a duplicate', student_profile['Name'])
					duplicates_found += 1
					logger.info('Found [%s] duplicates', duplicates_found)

				# Break from creating students in this school
				# if duplicates surpass number of students needed in school
				if duplicates_found > 2000:
					skipped_students += (1000 - index)
					logger.info('Skipped generating %s students for %s because of too many duplicates', 1000 - index, school['Name'])
					break

		CsvWriter.write(data=student_profiles)
		logger.info('Csv file generated successfully. Skipped %s student(s)', skipped_students)