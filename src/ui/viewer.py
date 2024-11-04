import PySimpleGUI as sg

bold_font = ('Helvetica', 12, 'bold')


def show_popup(broken_addressees, messaged_users, messaged_before):
    popup_layout = [
        [sg.Text('Broken Addressees', font=bold_font)],
        [sg.Listbox(values=broken_addressees, size=(40, 10), key='-BROKEN-ADDRESSEES-', enable_events=True)],
        [sg.Text('Messaged Users', font=bold_font)],
        [sg.Listbox(values=messaged_users, size=(40, 10), key='-MESSAGED-USERS-', enable_events=True)],
        [sg.Text('Messaged Before', font=bold_font)],
        [sg.Listbox(values=messaged_before, size=(40, 10), key='-MESSAGED-USERS-', enable_events=True)],
        [sg.Button('Close', key='-CLOSE-')]
    ]

    popup_window = sg.Window('Popup Window', popup_layout)

    while True:
        event, values = popup_window.read()

        if event in (sg.WINDOW_CLOSED, '-CLOSE-'):
            break

    popup_window.close()



def ask_for_2fa():
    layout = [
        [sg.Text('Please enter your 2FA code:', font=bold_font)],
        [sg.Input(key='-CODE-')],
        [sg.Button('Submit')],
    ]
    sg.theme('SandyBeach')

    window = sg.Window('2FA Code Entry', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            window.close()
            return None
        elif event == 'Submit':
            code = values['-CODE-']
            window.close()
            return code
        else:
            window.close()
    
def popup_acsl_add():
    username = None
    password = None
    layout = [
        [sg.Text('username', font=bold_font), sg.Input(key='-ACSL-ADD-USERNAME-')],
        [sg.Text('password', font=bold_font), sg.Input(key='-ACSL-ADD-PASSWORD-')],
        [sg.Push(), sg.Button('OK', key='-ACSL-ADD-OK-', enable_events=True)],
    ]
    window = sg.Window('POPUP', layout, modal=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-ACSL-ADD-OK-':
            username = values['-ACSL-ADD-USERNAME-']
            password = values['-ACSL-ADD-PASSWORD-']
            break
    window.close()
    return username, password


# layout is a list of lists
def layout(account_list, addressee_set_list, message_set_list):
    top_layout = [
        # columns keep vertically separated blocks
        sg.Column(
            [
                [
                    sg.Text('Accounts', font=bold_font),
                ],
                [
                    # without enable_events, nothing would hapen on selection
                    sg.Listbox(account_list, size=(40, 10), key='-ACSL-', enable_events=True, expand_x=True),
                ],
                [
                    sg.Button('Delete', key='-ACSL-DEL-', button_color=('red', 'white')),
                    sg.Button('Add', key='-ACSL-ADD-'),
                    # file browser doesn't emit events, it updates the specified element.
                    # In order for an event to happen when a file is selected, the target element has to have
                    # enable_events=True
                    sg.Input(key='-ACSL-UPL-', visible=False, enable_events=True),
                    sg.FileBrowse(button_text='Upload',
                                  target='-ACSL-UPL-',
                                  file_types=[
                                      ("Accepted Files", "*.csv *.xlsx")]),
                ]
            ],
            expand_x=True),
        sg.VerticalSeparator(),
        sg.Column(
            [
                [
                    sg.Text('Addressees', font=bold_font),
                ],
                [
                    sg.Listbox(addressee_set_list, size=(40, 10), key='-ADSL-', enable_events=True, expand_x=True),
                ],
                [
                    sg.Button('Delete', key='-ADSL-DEL-', button_color=('red', 'white')),
                    sg.Input(key='-ADSL-UPL-', visible=False, enable_events=True),
                    sg.FileBrowse(button_text='Upload', target='-ADSL-UPL-',
                                  file_types=[("Accepted Files", "*.csv *.xlsx")]),
                ]
            ],
            expand_x=True
        ),
        sg.VerticalSeparator(),
        sg.Column(
            [
                [
                    sg.Text('Messages', font=bold_font)
                ],
                [
                    sg.Listbox(message_set_list, size=(40, 10), key='-MSL-', enable_events=True, expand_x=True),
                ],
                [
                    sg.Button('Delete', key='-MSL-DEL-', button_color=('red', 'white')),
                    sg.Input(key='-MSL-UPL-', visible=False, enable_events=True),
                    sg.FileBrowse(button_text='Upload', target='-MSL-UPL-',
                                  file_types=[("Accepted Files", "*.csv *.xlsx")]),
                ]
            ],
            expand_x=True
        )
    ]

    bottom_layout = [
        [sg.Text('Sending from:', font=bold_font, key='-SF-')],
        # [sg.Listbox(values=[], size=(None, 10), key='-MOL-', enable_events=True, expand_x=True, expand_y=True)],
        [sg.Table(values=[], headings=['usernames', 'names', 'messages'], col_widths=[20, 20, 60], auto_size_columns=False,
                   key='-MOL-', enable_events=True, expand_x=True, expand_y=True, justification='left',
                  # size=(None, 10)
                  )],

        sg.Column([[sg.Text('Check if addressee has been messaged before:', font=bold_font, pad=0),
                    sg.Checkbox('', key='-ATB-', enable_events=True, pad=0)]],
                  justification='center'),
        sg.VerticalSeparator(),
        sg.Column([[sg.Button('Start', key='-START-', button_color=('white', 'green'), size=20)]], justification='center'),
        sg.VerticalSeparator(),
        sg.Column([[sg.Text('Headless Mode:', font=bold_font, pad=10),
                    sg.Checkbox('', key='-HED-', enable_events=True, pad=0)]],
                  justification='right'),
    ]

    layout = [
        #  this ensures horizontal separation
        [top_layout, [sg.HSeparator()], bottom_layout]
    ]
    # return sg.Window('ProjectTBD', layout, size=(1500, 300), resizable=True)
    return sg.Window('Hi-Tech', layout, resizable=True)
