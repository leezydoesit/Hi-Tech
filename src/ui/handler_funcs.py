from pathlib import Path
import PySimpleGUI as sg
from src.data.data_models import Account
from src.data.account_manager import get_account_data_by_username, save_new_account, get_usernames, remove_account
from src.data.addressee_manager import get_saved_addressee_sets, save_addressee_set, get_saved_addressee_set_names, \
    remove_addressee_set, get_addressee_set_for_set_name
from src.data.message_manager import remove_message_set, get_saved_message_set_names, save_message_set, \
    get_messages_for_set_name
from src.exceptions import PTBDException, log_error
from src.config.logger import logger
from src.data.file_handling import df_from_file, check_file_type
from src.ui.viewer import popup_acsl_add


def select_account(values, window, automation_data):
    """
    runs when a row is selected in the accounts listbox
    :param values: UIState values
    :param window: sg.window
    :param automation_data: hold credentials and messages
    :return: Nothing
    """
    logger.debug('Account selected')
    # select the account
    try:
        selected_username = values['-ACSL-'][0]
    except IndexError:
        logger.debug('No accounts listed in the window')
        return
    account_data = get_account_data_by_username(selected_username)
    if account_data is not None:
        logger.debug(f'found account data for {selected_username}')
        logger.debug(f'account data: {account_data}')
        automation_data.credentials = Account(
            **account_data
        )
        # check if there is session data
        logger.debug(f'automation data: {automation_data}')
        if automation_data.credentials.session is not None:
            msg = f'Sending from {selected_username} (has session data)'
        else:
            msg = f'Sending from {selected_username} (no session data)'
        # update the UI above the big message list
        window['-SF-'].update(f'{msg}')
    else:
        logger.debug(f'no account data found for {selected_username}')


def add_account(window):
    """
    Runs when the Add button under the accounts list is clicked
    :param window: sg.Window
    :return: Nothing
    """
    logger.debug('Asking for new account details')
    # run a pop up to ask for a credentials
    logger.debug('New account data submitted, going to save')
    username, password = popup_acsl_add()
    try:
        save_new_account(username, password)
    except PTBDException:
        pass
    # refresh the accounts list
    window['-ACSL-'].update(get_usernames())
    

def del_account(values, window):
    """
    runs when the Delete button under the account listbox is clicked
    :param values: values associated with the current state of the window
    :param window: sg.window
    :return: Nothing
    """
    try:
        acc_to_delete = values['-ACSL-'][0]
    except IndexError:
        # probably no account was selected
        log_error('No account selected')
        return
    logger.debug(f'Asked to delete account {acc_to_delete}')
    confirm_delete = sg.popup_ok_cancel('Are you sure you want to delete this account?')
    if confirm_delete == 'OK':
        logger.debug(f'Confirmed deleting account {acc_to_delete}')
        # delete the account using account manager
        remove_account(acc_to_delete)
        # update the accounts list
        window['-ACSL-'].update(get_usernames())
        # remove the "Sending form " name, it's the one we just deleted
        window['-SF-'].update('Sending from:')


def upload_accounts(values, window):
    """
    Runs when the upload button under the accounts listbox is clicked
    :param window: sg.window
    :param values: values associated with the current state of the window
    :return: Nothing
    """
    file_path = Path(values['-ACSL-UPL-'])
    if check_file_type(file_path, ['.csv', '.xlsx']):
        try:
            df = df_from_file(file_path, ['username', 'password'])
            df.apply(lambda row: save_new_account(row['username'], row['password'], in_dataframe=True), axis=1)
            window['-ACSL-'].update(get_usernames())
        except (PTBDException, FileNotFoundError):
            # user has been notified about the error in a popup
            pass


def del_addressee_set(values, window):
    """
    Runs when the Delete button under the addressee listbox is clicked
    :return:
    """
    try:
        adr_to_delete = values['-ADSL-'][0]
    except IndexError:
        # probably no account was selected
        log_error('No account selected')
        return
    logger.debug(f'Asked to delete addressee set {adr_to_delete}')
    confirm_delete = sg.popup_ok_cancel('Are you sure you want to delete this addressee set?')
    if confirm_delete == 'OK':
        logger.debug(f'Confirmed deleting addressee set {adr_to_delete}')
        # delete the account using account manager
        remove_addressee_set(adr_to_delete)
        # update the accounts list
        window['-ADSL-'].update(get_saved_addressee_set_names())


def upload_addressee_sets(values, window):
    """
    Runs when the upload button under the accounts listbox is clicked
    :param window: sg.window
    :param values: values associated with the current state of the window
    :return: Nothing
    """
    file_path = Path(values['-ADSL-UPL-'])
    if check_file_type(file_path, ['.csv', '.xlsx']):
        try:
            df = df_from_file(file_path, ['username', 'name'])
            save_addressee_set(df, file_path.stem)
            window['-ADSL-'].update(get_saved_addressee_set_names())
        except (PTBDException, FileNotFoundError):
            # user has been notified about the error in a popup
            pass


def display_addressees_from_set(set_name, window):
    """
    When an addressee set is selected in the addressee set listbox,
    its addressees are shown in the addressee and message window at the bottom
    :return: Nothing
    """
    logger.debug(f'Displaying addressees for set {set_name}')
    addressees = get_addressee_set_for_set_name(set_name, names_only=True)
    window['-MOL-'].update(addressees)


def del_message_set(values, window):
    """
    Runs when the Delete button under the message listbox is clicked
    :return:
    """
    try:
        msg_to_delete = values['-MSL-'][0]
    except IndexError:
        # probably no message set was selected
        log_error('No message set selected')
        return
    logger.debug(f'Asked to delete message set {msg_to_delete}')
    confirm_delete = sg.popup_ok_cancel('Are you sure you want to delete this message set?')
    if confirm_delete == 'OK':
        logger.debug(f'Confirmed deleting message set {msg_to_delete}')
        # delete the account using account manager
        try:
            remove_message_set(msg_to_delete)
        except PTBDException:
            pass
        # update the accounts list
        window['-MSL-'].update(get_saved_message_set_names())


def upload_message_sets(values, window):
    """
    Runs when the upload button under the message listbox is clicked
    :param window: sg.window
    :param values: values associated with the current state of the window
    :return: Nothing
    """
    file_path = Path(values['-MSL-UPL-'])
    if check_file_type(file_path, ['.csv', '.xlsx']):
        try:
            df = df_from_file(file_path, ['message'])
            save_message_set(df, file_path.stem)
            window['-MSL-'].update(get_saved_message_set_names())
        except (PTBDException, FileNotFoundError):
            # user has been notified about the error in a popup
            pass


def display_messages_from_set(set_name, window):
    """
    When an message set is selected in the addressee set listbox,
    its messages are shown in the addressee and message window at the bottom
    :return: Nothing
    """
    messages = get_messages_for_set_name(set_name)
    # the table has 3 columns, we only have one
    # if we are populating this way, it means that the addressee columns are empty
    table_data = [['', '', m] for m in messages]
    window['-MOL-'].update(table_data)


def select_addressee_and_message_sets(event, values, window, automation_data):
    """
    When the addressee and message sets are selected in the addressee and message window,
    the message objects will be shown in the message table. Otherwise, either the messages
    or the addressess only will be shown.
    :param event: the event that was emitted by the ui
    :param values: value stack
    :param window: current window
    :param automation_data: object holiding credentials and message objects
    :return:
    """
    if values.get('-MSL-', False) and values.get('-ADSL-', False):
        message_set = values['-MSL-'][0]
        addressee_set = values['-ADSL-'][0]
        # create the message data and pass it to the table
        automation_data.make_message_obj(addressee_set, message_set)
        window['-MOL-'].update(automation_data.table_data)
    else:
        # if a message set is selected, prepare the whole addressee-message table
        # no message set selected, just list the addressees
        if values.get(event, False):
            value = values[event][0]
            if event == '-ADSL-':
                display_addressees_from_set(value, window)
            elif event == '-MSL-':
                display_messages_from_set(value, window)
            logger.debug(f'No messages listed in the window. Values MSL: {values["-MSL-"]}')
