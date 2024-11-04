from multiprocessing import Process
from src.bot.IgBot import IgBot
from src.config.logger import logger
from src.data.addressee_manager import get_saved_addressee_set_names
from src.data.message_manager import get_saved_message_set_names
from src.ui.ui_state import UIState
import PySimpleGUI as sg
from src.data.account_manager import get_usernames
from src.data.automation_data import AutomationData
from src.ui.handler_funcs import select_account, add_account, del_account, upload_accounts, del_addressee_set, \
    upload_addressee_sets, del_message_set, upload_message_sets, select_addressee_and_message_sets

def start_bot(automation_data):
    """
    Runs IgBot. This function is to be called as a new process.
    :param automation_data: instance with credentials, messages etc
    :return: nothing
    """
    igBot = IgBot(automation_data)
    igBot.run()  # Just call the run method once, it contains the loop


def event_handlers(ui_state, automation_data):
    """
    # this function will be called to decide which action to take
    # given an event
    :param ui_state: holds the window, event and values
    :param automation_data: will have credentials and messages with addresses
    :return: nothing
    """
    # make the code more concise by not referencing the object
    event = ui_state.event
    values = ui_state.values
    window = ui_state.window
    if event == '-ACSL-':
        # account selection
        select_account(values, window, automation_data)
    elif event == '-ACSL-ADD-':
        # add a new account
        add_account(window)
    elif event == '-ACSL-DEL-':
        # delete the selected account
        del_account(values, window)
    elif event == '-ACSL-UPL-':
        # upload a file with account information
        upload_accounts(values, window)
    elif event in ['-MSL-', '-ADSL-']:
        # if both are selected, creates message objects for sending, otherwise displays values
        select_addressee_and_message_sets(event, values, window, automation_data)
    elif event == '-ADSL-DEL-':
        # delete the selected addressee set
        del_addressee_set(values, window)
    elif event == '-ADSL-UPL-':
        # upload a file with addressee information
        upload_addressee_sets(values, window)
    elif event == '-MSL-DEL-':
        # delete the selected message set
        del_message_set(values, window)
    elif event == '-MSL-UPL-':
        # upload a file with message information
        upload_message_sets(values, window)
    elif event == '-ATB-':
        # the checkbox is selected or deselected
        automation_data.check_messaged_before = values['-ATB-']
    elif event == '-HED-':
        if values['-HED-']:
            automation_data.headless = True
        if not values['-HED-']:
            automation_data.headless = False


def run():
    sg.theme('SandyBeach')
    automation_data = AutomationData()
    account_list = get_usernames()
    addressee_set_list = get_saved_addressee_set_names()
    message_set_list = get_saved_message_set_names()
    ui_state = UIState(account_list, addressee_set_list, message_set_list)
    processes = []
    while True:
        ui_state.update()
        # window closed, shut down
        if ui_state.event == sg.WINDOW_CLOSED:
            break

        # start a new IgBot process
        elif ui_state.event == '-START-':
            # start the automation
            # check if the needed data is selected
            if automation_data.credentials is not None and automation_data.message_obj != []:
                logger.debug(f"Starting the automation, with the data {automation_data}")
                p = Process(target=start_bot, args=(automation_data,))
                p.start()
                processes.append(p)
            else:
                sg.popup('Please select an account, an addressee set and a message set and a message set')
        event_handlers(ui_state, automation_data)

    # the main process will wait for all processes to finish
    # the gui window can be closed, it will still wait
    for p in processes:
        p.join()
    ui_state.window.close()
