import json
import PySimpleGUI as sg
from pandas import read_csv, read_excel, DataFrame
from pandas.errors import EmptyDataError, ParserError
from pathlib import Path
from src.config.logger import logger
from src.exceptions import PTBDException


def df_from_file(file_path: Path, required_columns: list):
    """
    Given a file path, return a dataframe. File must be one of CSV, XLSX,
    or TXT. if a TXT is given, only one column can be used.
    :param file_path: path to the file
    :param required_columns: column heading, list of string(s)
    :return: dataframe
    """
    logger.debug(f'Reading file {file_path}')
    suffix = file_path.suffix.lower()
    df = DataFrame()

    if suffix == '.csv':
        logger.debug('file is a CSV')
        try:
            df = read_csv(file_path)
        except FileNotFoundError:
            raise PTBDException(f'{file_path} not found')
        except ValueError:
            raise PTBDException(f"Error, can't read the CSV {file_path}, check if it's corrupted or empty")

    elif suffix == '.xlsx':
        logger.debug('file is a XLSX')
        try:
            df = read_excel(file_path)
        except EmptyDataError:
            raise PTBDException(f"Error, can't read the Excel file {file_path}, check if it's corrupted or empty")
        except ParserError:
            raise PTBDException(f"Error, the Excel file {file_path} is malformed")
        except Exception as e:
            raise PTBDException(f"An error occurred while reading the Excel file {file_path}: {str(e)}")

    found_columns = list(df)
    # check that the columns match the requirement
    if len(set(found_columns).intersection(required_columns)) != len(required_columns):
        raise PTBDException(f'the columns identified in {file_path} do not match the required "{required_columns}"')

    return df


def json_files_to_list(directory: Path, index_file_names=False):
    """
    Given a folder, it reads oll Json files in that folder
    :param directory: path to the folder
    :param index_file_names: if True, the file names are used as the indices
    :return: None if there are no .json files
    :return: a list the contents of the json files
    ------------------------
    """
    logger.debug(f"reading json file from the dir {directory} to list")
    found_data = []
    try:
        for c_file in directory.glob('*.json'):
            with open(c_file) as f:
                # load the file into a structure
                file_contents = json.load(f)
                if index_file_names:
                    # add the set name to the set
                    found_data.append({'set_name': c_file.stem, 'data': file_contents})
                else:
                    found_data.append(file_contents)
    except PermissionError as e:
        logger.error(f"Couldn't retrieve the store data, possibly {directory} isn't executable. {e}")

    if not found_data:
        logger.debug("No saved data found")
        return []

    logger.debug(f"Found saved data: {found_data}")
    return found_data


def check_file_type(file_path, extensions):
    """
    Checks if the file is a valid file, if not pops up an error an error
    :param file_path: the path to the file
    :param extensions: list of valid extensions
    :return: True or False
    """
    if file_path.suffix.lower() not in extensions:
        error_msg = f'{file_path.suffix} is not a valid file type'
        logger.error(error_msg)
        sg.popup_error(error_msg)
        return False
    return True
