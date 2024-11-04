import os
from pathlib import Path

from src.config.config import config
from src.config.logger import logger
from src.data.file_handling import json_files_to_list
from src.exceptions import PTBDException, log_error


def get_saved_addressee_sets():
    """
    Obtains the list of saved addressee sets
    This is just a wrapper func around json_files_to_list, but
    it's a good idea to have it here, as it concerns addressee management
    :return: None if there are no .json files
    :return: saved_accounts
    ------------------------
    """
    logger.debug("Get Saved Addressee Sets")
    saved_addressee_sets = json_files_to_list(config.addressee_sets_dir, index_file_names=True)
    return saved_addressee_sets


def get_saved_addressee_set_names():
    """
    Gets just the names of each set, rather than the full dict
    :return: None if there are no .json files
    :return: saved_accounts names
    """
    logger.debug("Get Saved Addressee Sets Names")
    try:
        saved_addressee_set_names = [s['set_name'] for s in get_saved_addressee_sets()]
    except TypeError:
        # no saved addressee sets
        logger.debug("No saved addressee sets")
        saved_addressee_set_names = []
    return saved_addressee_set_names


def save_addressee_set(df, file_name):
    """
    Creates a new addressee set file from the dataframe    :param df:
    :param file_name: the name of the original set
    :return: None
    """
    logger.debug("Creating a new addressee set")
    new_addressee_set_path = Path(config.addressee_sets_dir, f'{file_name}.json')
    if new_addressee_set_path.exists():
        raise PTBDException(f"Addressee set {file_name} already exists, cannot import")
    df.to_json(new_addressee_set_path, orient="records")


def remove_addressee_set(set_name):
    """
    Removes the addressee set
    :param set_name: then name of the file
    :return: Nothing
    """
    logger.debug("Started remove addressee")
    """
    Removes the addressee set file for the given name    
    """
    set_path = Path(config.addressee_sets_dir, f'{set_name}.json')
    try:
        os.remove(set_path)
        # refresh the window below, as it now shows addressees from the deleleted set
        # TODO:
    except PermissionError:
        raise PTBDException(f"Couldn't delete the addressee set file '{set_path}'")


def get_addressee_set_for_set_name(set_name, names_only=False):
    """
    Given the set name, it tries to find the addressee set file of the same name and returned its
    contents
    :param set_name: the stem of the addressee file name, shown in the middle top window
    :param names_only: if True, only the usernames and names of the addressee set is returned
    :return: Addressees
    :return: Nothing
    """
    try:
        named_set = list(filter(lambda s: s['set_name'] == set_name, get_saved_addressee_sets()))
        if names_only:
            # break the names and usernames from the data
            res = []
            for d in named_set:
                for dd in d['data']:
                    res.append([dd['username'], dd['name']])
            return res
        return named_set
    # except TypeError:
    except IndexError:
        log_error(f"File for the addressee set '{set_name}' not found")
        return None



