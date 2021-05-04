import os
import sys
from DataGenerator import DataGenerator
from utility import logger, current_time


def parse_inputs(arguments):
    '''
        in this method we are: 
            1. fetching command line arguments like iteration count value, 
                file path and list of field name and data type;
            2. splitting arguments to fetch value of count, path, field name and data type
            3. storing the values in correct variables.
    '''
    try:
        lists_after_splitting_arguments = []
        count = 100
        path = None
        field_and_data_type_list = []

        # splitting arguments after main.py to fetch value of count and path in list
        for argument in arguments[1:]:
            lists_after_splitting_arguments.append(argument.split("="))

        # assigning value to count, path and list of field name and data type
        for list_of_argument in lists_after_splitting_arguments:
            if list_of_argument[0] == 'count':
                count = int(list_of_argument[1]) if str(
                    list_of_argument[1]).isdigit() else 100
            elif list_of_argument[0] == 'path':
                path = list_of_argument[1]
            else:
                field_and_data_type_list += list_of_argument

        return count, path, field_and_data_type_list

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    try:
        # to compute execution time
        begin_time = current_time()

        # processing command line argument
        count, path, field_and_data_type_list = parse_inputs(sys.argv)

        processed_data = []

        if not(path) and not field_and_data_type_list:
            # consider the scenario: script with default params
            # if path is not given then the data file from the input folder will be considered
            # please keep the default file to be accessed in input folder (create if doesn't exist)

            path = os.path.abspath(os.getcwd())
            path += '/input/data.xlsx'

        # check if the given file path exist else raise exception
        if path:
            if not os.path.exists(path):
                raise Exception("Path is invalid")

            # splitting the file path to get file name and it's extension
            file_name = "".join(path).split("/")[-1]

            file_extension = file_name.split(".")[-1]

            # extracting data according to file extension
            if file_extension not in ["xls", "xlsx", "odt", "ods"]:
                logger.error(
                    "Given format file is invalid, please provide excel compatible file")

        datagenerator_obj = DataGenerator(count, path)
        processed_data = datagenerator_obj.read_xls_data()

        if field_and_data_type_list:

            # this code is to process fetched field name and datatype from console
            field_data_type_tuple = ()

            for element in field_and_data_type_list:
                field_data_type_tuple += (element,)
                if str(element).lower().strip() == 'value':
                    continue
                if len(field_data_type_tuple) >= 2:
                    processed_data.append(field_data_type_tuple)
                    field_data_type_tuple = ()

        if processed_data:
            datagenerator_obj.create_files(processed_data)

            minute, second = divmod(current_time()-begin_time, 60)

            logger.info("Execution of {} records ended in : {:0.0f} minute {:0.02f} second".format(
                count, minute, second))

        logger.info("End of script....")

    except Exception as e:
        logger.error(e)
