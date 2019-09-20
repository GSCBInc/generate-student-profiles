import csv
import os


class CsvReader:

    fieldnames = ['Name', 'Phone', 'Address']
    folder = 'data/'

    @staticmethod
    def read(file_name='schools.csv'):
        file_handle = open(CsvReader.folder + file_name, 'r')
        data = []

        reader = csv.DictReader(file_handle)
        for row in reader:
            school = {}
            for prop in CsvReader.fieldnames:
                school[prop] = row[prop]

            data.append(school)

        file_handle.close()

        return data


class CsvWriter:

    fieldnames = [
        'Name', 'School', 'Grade', 'Date of Birth', 'Lep',
        'Student Id', 'Designation', 'Sex', 'Reduced lunch fee', 'Race'
    ]
    folder = 'output/'

    @staticmethod
    def write_list(writer, data):
        if data is not None:
            for d in data:
                writer.writerow(d)

    @staticmethod
    def write(file_name='students.csv', data=None):
        if not os.path.exists(CsvWriter.folder):
            os.mkdir(CsvWriter.folder)

        if os.path.exists(CsvWriter.folder + file_name):
            file_handle = open(CsvWriter.folder + file_name, 'a', newline='')
        else:
            file_handle = open(CsvWriter.folder + file_name, 'w', newline='')

        writer = csv.DictWriter(file_handle, fieldnames=CsvWriter.fieldnames)

        if file_handle.mode == 'w':
            writer.writeheader()

        CsvWriter.write_list(writer, data)
        file_handle.close()
