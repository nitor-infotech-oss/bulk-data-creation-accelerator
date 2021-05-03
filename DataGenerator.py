import os
import pandas as pd
import random
from alive_progress import alive_bar
from mapping import faker_function_dictionary, random_value_dictionary
from utility import logger, datetime_now, data_frame


class DataGenerator:

    def __init__(self, iteration_count=100, file_path=None):
        '''
            initialization method to set count and path parameters
        '''
        try:
            self.iteration_count = iteration_count
            if file_path and os.path.exists(file_path):
                self.path = file_path
            else:
                self.path = None
        except Exception as e:
            logger.error(e)

    def generate_data(self, processed_data):
        '''
            in this method we are normalizing data and creating an Ordered Dictionary of generated data
            i.e. generation of data from processed data in ordered format.
            created mapping using Faker Library.
        '''
        try:
            gender_list = []
            first_name_list = []
            full_name_list = []

            with alive_bar(len(processed_data)) as bar:
                for field in processed_data:
                    value_list = []
                    field_name = field[0]
                    data_type = field[1]

                    # if field's value is given in excel then appending provided records
                    if '=' in data_type:
                        value_list = [data_type.split('=')[-1] for iteration in range(
                            self.iteration_count)]

                    # if field's value is given in excel then appending provided records
                    elif len(field) > 2:
                        value_list = [field[2] for iteration in range(
                            self.iteration_count)]

                    # to get value from faker library's dictionary
                    elif faker_function_dictionary.get(str(data_type).lower()):
                        for iteration in range(self.iteration_count):
                            value_list.append(
                                faker_function_dictionary[data_type]())

                    # to get value from random dictionary
                    elif random_value_dictionary.get(str(data_type).lower()):
                        for iteration in range(self.iteration_count):
                            value_list.append(random.choice(
                                random_value_dictionary[str(data_type).lower()]))

                    # if field's data type is invalid then appending empty records
                    else:
                        value_list = [None for iteration in range(
                            self.iteration_count)]

                    data_frame.update({field_name: value_list})

                    # These lines are to correct gender with respect to first name in further processing
                    if data_type == 'gender':
                        gender_list = data_frame[field_name]
                    if data_type == 'first_name':
                        first_name_key = field_name
                        first_name_list = data_frame[field_name]
                    if data_type == 'name':
                        full_name_key = field_name
                        full_name_list = data_frame[field_name]
                    bar()

            if gender_list:
                for position in range(len(gender_list)):
                    if first_name_list:
                        # this logic will check and replace first name value according to gender
                        if gender_list[position] == 'male':
                            first_name_list[position] = faker_function_dictionary['first_name_male']()
                        elif gender_list[position] == 'female':
                            first_name_list[position] = faker_function_dictionary['first_name_female']()

                    if full_name_list:
                        # this logic will check and replace full name value according to gender
                        if gender_list[position] == 'male':
                            full_name_list[position] = faker_function_dictionary['name_male']()
                        elif gender_list[position] == 'female':
                            full_name_list[position] = faker_function_dictionary['name_female']()

                if first_name_list:
                    data_frame[first_name_key] = first_name_list
                if full_name_list:
                    data_frame[full_name_key] = full_name_list

            return data_frame

        except Exception as e:
            logger.error(e)

    def read_xls_data(self):
        '''
            in this method we are reading xls data from given location in the path variable.
            fetch the field name and its data type from the raw string and converting it to list of tuples.
            basically, converting the raw data to processed data.
        '''
        try:
            if self.path:
                logger.info("Reading data from >>> {}".format(self.path))
                raw_data = pd.read_excel(self.path, usecols="A:B")
                processed_data = []

                field_name = raw_data.get('fieldname')
                data_type = raw_data.get('dataType')

                # fetching field name and data type from raw data
                if str(field_name) != 'None' and str(data_type) != 'None' and field_name.size == data_type.size:
                    field_name_list = raw_data['fieldname'].tolist()
                    data_type_list = raw_data['dataType'].tolist()

                    for position in range(0, len(field_name_list)):
                        # appending column name with it's data type in a tuple format
                        processed_data.append((field_name_list[position], data_type_list[position]))

                else:
                    logger.info("Invalid input excel file")

                return processed_data

            else:
                return []

        except Exception as e:
            logger.error(e)

    def create_files(self, processed_data):
        '''
            in this function we are accepting data and converting it to data frame of pandas library 
            and generating 3 output files as excel, csv and json
            "params":
                processed_data: should be in the format : [(field name, data type),(field name, data type)....]
        '''
        try:
            if processed_data:
                generated_data = self.generate_data(processed_data)
                data_frame_object = pd.DataFrame(generated_data)

                # creating output directory if it doesn't exist
                if not os.path.exists('./output'):
                    os.makedirs('./output')

                # clearing output folder's previous files
                current_path = os.path.abspath(os.getcwd())+"/output/"
                for files in os.listdir(current_path):
                    os.remove(current_path+files)

                # creating 3 files in output folder with generated data
                data_frame_object.to_excel('./output/excel_data_{}.xlsx'.format(
                    datetime_now.strftime("%Y%m%d-%I%M%S%p")), index=False)

                data_frame_object.to_csv("./output/csv_data_{}.csv".format(
                    datetime_now.strftime("%Y%m%d-%I%M%S%p")), index=False)

                data_frame_object.to_json("./output/json_data_{}.json".format(
                    datetime_now.strftime("%Y%m%d-%I%M%S%p")), orient='records')

                logger.info("Files created successfully")

            else:
                logger.error("Data generation failed")

        except Exception as e:
            logger.error(e)
