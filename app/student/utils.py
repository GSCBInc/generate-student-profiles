import datetime
import logging
import random
import re

logger = logging.getLogger(__name__)


class Generator:

    last_student_id = 0

    grades = [
        # Elementary school grades | range (0, 6)
        'Pre-Kindergarten', 'Kindergarten', '1st', '2nd', '3rd', '4th',

        # Middle school grades | range (6, 10)
        '5th', '6th', '7th', '8th',

        # High school grades | range (10, 14)
        '9th', '10th', '11th', '12th'
    ]

    is_lep = ['Yes', 'No']

    designation = ['None', 'Special Ed', '504']

    ethnicity = [
        'Hispanic or Latino', 'Hispanic', 'Latino',
        'American Indian', 'Indian', 'American',
        'Alaskan Native', 'Alaskan', 'Asian',
        'Native Hawaiian', 'Hawaiian', 'Black',
        'Black or African American', 'African',
        'African American', 'White', 'Caucasian',
        'White or Caucasian', 'Not Disclosed'
    ]

    sex = ['Male', 'Female']

    has_reduced_lunch = ['Yes', 'No']

    months_max_days = {
        1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    grade_to_year = {
        'Pre-Kindergarten': 2015,
        'Kindergarten': 2014,
        '1st': 2013,
        '2nd': 2012,
        '3rd': 2011,
        '4th': 2010,
        '5th': 2009,
        '6th': 2008,
        '7th': 2007,
        '8th': 2006,
        '9th': 2005,
        '10th': 2004,
        '11th': 2003,
        '12th': 2002
    }

    @staticmethod
    def student_grade(school_name):
        student_grade = Generator.grades[random.randrange(0, 14)]

        if re.match(r'.*High.*', school_name):
            student_grade = Generator.grades[random.randrange(10, 14)]

        elif re.match(r'.*Middle.*', school_name):
            student_grade = Generator.grades[random.randrange(6, 10)]

        elif re.match(r'.*Elementary.*', school_name):
            student_grade = Generator.grades[random.randrange(0, 6)]

        return student_grade

    @staticmethod
    def student_date_of_birth(student_grade):
        year = Generator.grade_to_year[student_grade]
        month = random.randrange(1, 13)
        day = random.randrange(1, Generator.months_max_days[month])

        date_of_birth = datetime.datetime(year, month, day).strftime('%m/%d/%Y')
        return date_of_birth

    @staticmethod
    def randomly_select(selection_list):
        return selection_list[random.randrange(len(selection_list))]

    @staticmethod
    def student_is_lep():
        return Generator.randomly_select(Generator.is_lep)

    @staticmethod
    def student_designation():
        return Generator.randomly_select(Generator.designation)

    @staticmethod
    def student_sex():
        return Generator.randomly_select(Generator.sex)

    @staticmethod
    def student_ethnicity():
        return Generator.randomly_select(Generator.ethnicity)

    @staticmethod
    def student_has_reduced_lunch():
        return Generator.randomly_select(Generator.has_reduced_lunch)

    @staticmethod
    def student_id():
        Generator.last_student_id += 1
        return Generator.last_student_id


class Transformer:

    @staticmethod
    def get_first_name(student):
        if type(student) is str:
            first_name = student.split(' ')[0]
        else:
            first_name = student['name']['first']

        return first_name.capitalize()

    @staticmethod
    def get_last_name(student):
        if type(student) is str:
            last_name = student.split(' ')[1]
        else:
            last_name = student['name']['last']

        return last_name.capitalize()

    @staticmethod
    def create_full_name(student):
        return Transformer.get_first_name(student) + ' ' + Transformer.get_last_name(student)

    @staticmethod
    def create_student_profile(student, school):
        student_grade = Generator.student_grade(school['Name'])
        return {
            'Name': Transformer.create_full_name(student),
            'School': school['Name'],
            'Grade': student_grade,
            'Designation': Generator.student_designation(),
            'Lep': Generator.student_is_lep(),
            'Student Id': Generator.student_id(),
            'Date of Birth': Generator.student_date_of_birth(student_grade),
            'Reduced lunch fee': Generator.student_has_reduced_lunch(),
            'Race': Generator.student_ethnicity(),
            'Sex': Generator.student_sex()
        }
