from src.ui.viewer import layout


class UIState:
    """
    Captures the current state of the UI, the window, events, etc
    """

    def __init__(self,
                 account_list: list,
                 addressee_set_list: list,
                 message_set_list: list):
        self.window = layout(account_list,
                             addressee_set_list,
                             message_set_list)
        self.event = None
        self.values = None

    def update(self):
        """
        to be called inside the main UI loop
        reads event and values from the window and stores them
        :return: Nothing
        """
        self.event, self.values = self.window.read()


