import json
import os
from pathlib import Path

from src.config.config import config
from src.config.logger import logger
from src.data.file_handling import json_files_to_list
from src.exceptions import PTBDException, log_error


def get_saved_accounts():
    """
    Obtain the list of saved accounts
    This is just a wrapper func around json_files_to_list, but 
    it's a good idea to have it here, as it concerns account management
    :return: None if there are no .json files
    :return: saved_accounts
    ------------------------
    """
    logger.debug("Get Saved Accounts")
    saved_accounts = json_files_to_list(config.accounts_dir)
    logger.debug("Saved Accounts: " + str(saved_accounts))
    return saved_accounts


def get_account_data_by_username(username):
    """
    Selects the account data for the given username, if it exists
    :return: None if there are no .json files
    :return: saved_accounts
    ------------------------
    Example:
        [{'username': username, 'password': password, 'session': ''}, {...}]
    
    Obs.: The session object is set when the user logs in
    """
    logger.debug(f"Getting account data for {username}")
    saved_accounts = get_saved_accounts()
    for account in saved_accounts:
        if account['username'] == username:
            logger.debug(f"found {account} for {username}")
            return account
    return None


def save_new_account(new_user, new_password, session=None, in_dataframe=False) -> object:
    """
    Creates a new account file from username and password
    Checks if the username already exists in the accounts dir
    :rtype: object
    :param new_user: username
    :param new_password: password
    :param session: session, cookie
    :param in_dataframe: True if the dataframe is being used,
    this means that multiple accounts are being uploaded.
    If only some of the uploaded accounts exists, it will
    still upload the others, because an exception is ot going to be raised
    -----------------------
    Example:
        [{'username': username, 'password': password, 'session': ''}]
    """
    logger.debug("Creating a new account")
    # check if the username and password are not empty or None
    if new_user == '' or new_password == '' or new_user is None or new_password is None:
            raise PTBDException("Username and password cannot be empty")

    config.account_file_path = Path(config.accounts_dir, f"{new_user}.json")
    logger.debug(f"Using username {new_user}, password {new_password}")

    if config.account_file_path.exists():
        # check if the username already exists
        # if not in_dataframe = only a single account is being created
        if not in_dataframe:
            raise PTBDException(f"User '{new_user}' already exists")
        else:
            # this is an upload, if there are any accounts that are not created,
            # we still want to create them, so don't raise an exception, that
            # would break the execution of the apply function
            log_error(f"User '{new_user}' already exists")

    credentials = {'username': new_user, 'password': new_password, 'session': session}
    logger.debug(f"Creating and storing credentials in {config.account_file_path}")
    try:
        with open(config.account_file_path, "w") as new_file:
            json.dump(credentials, new_file)
    except FileNotFoundError as e:
        logger.error(f"Couldn't store credentials, possibly the {config.accounts_dir} folder doesn't exist. {e}")
    except PermissionError as e:
        logger.error(f"Couldn't store credentials, possibly {config.account_file_path} isn't writeable. {e}")


def save_or_update_account(account):
    """
    Updates the account file for the given account.username
    :param: an instance of account
    :return:
    """
    logger.debug("Updating account")
    account_file_path = Path(config.accounts_dir, f"{account.username}.json")
    if account_file_path.exists():
        logger.debug(f"Updating account file for {account.username}")
        os.remove(account_file_path)
    else:
        logger.debug(f"Creating account file for {account.username}")
    save_new_account(account.username, account.password, account.session)


def remove_account(username):
    logger.debug("Started remove account")
    """
    Removes the account file for the given username    
    """
    credentials_file = Path(config.accounts_dir, f"{username}.json")
    try:
        os.remove(credentials_file)
    except PermissionError:
        raise PTBDException(f"Couldn't delete the credentials file '{credentials_file}',")


def get_usernames():
    saved_accounts = get_saved_accounts()
    if not saved_accounts:
        return []
    return sorted([u['username'] for u in saved_accounts])
