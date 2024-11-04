import os
from pathlib import Path

from src.config.config import config
from src.config.logger import logger
from src.data.file_handling import json_files_to_list
from src.exceptions import PTBDException, log_error


def get_saved_message_sets():
    """
    Obtains the list of saved message sets
    This is just a wrapper func around json_files_to_list, but
    it's a good idea to have it here, as it concerns addressee management
    :return: None if there are no .json files
    :return: saved_accounts
    ------------------------
    """
    logger.debug("Get Saved Message Sets")
    saved_message_sets = json_files_to_list(config.message_sets_dir, index_file_names=True)
    return saved_message_sets


def get_saved_message_set_names():
    """
    Gets just the names of each set, rather than the full dict
    :return: None if there are no .json files
    :return: saved_message_set names
    """
    logger.debug("Get Saved Message Sets Names")
    try:
        saved_message_set_names = [message_set['set_name'] for message_set in get_saved_message_sets()]
    except TypeError:
        # no saved message sets
        logger.debug("No saved message sets")
        saved_message_set_names = []
    return saved_message_set_names


def save_message_set(df, file_name):
    """
    Creates a new message set file from the dataframe
    :param df: dataframe
    :param file_name: the name of the original set
    :return: None
    """
    logger.debug("Creating a new message set")
    new_message_set_path = Path(config.message_sets_dir, f'{file_name}.json')
    if new_message_set_path.exists():
        raise PTBDException(f"Message set {file_name} already exists, cannot import")
    df.to_json(new_message_set_path, orient="records")


def remove_message_set(set_name):
    """
    Removes the message set
    :param set_name: then name of the file
    :return: Nothing
    """
    logger.debug("Started remove message set")
    set_path = Path(config.message_sets_dir, f'{set_name}.json')
    try:
        os.remove(set_path)
        # refresh the window below, as it now shows message from the deleleted set
        # TODO:
    except (PermissionError, FileNotFoundError):
        raise PTBDException(f"Couldn't delete the message set file '{set_path}'")


def get_messages_for_set_name(set_name):
    """
    Given the set name, it tries to find the message set file of the same name and returned its
    contents
    :param set_name: the stem of the message file name, shown in the middle top window
    :return: Message set
    :return: Nothing
    """
    try:
        found_data = filter(lambda s: s['set_name'] == set_name, get_saved_message_sets())
        return [m['message']for d in found_data for m in d['data']]
    # except TypeError:
    except FileNotFoundError:
        log_error(f"File for the addressee set '{set_name}' not found")
        return None



