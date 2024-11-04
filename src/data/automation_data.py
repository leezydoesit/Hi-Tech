from dataclasses import dataclass, field
from typing import List
from src.data.addressee_manager import get_addressee_set_for_set_name
from src.data.message_manager import get_messages_for_set_name
from src.data.data_models import MessageObject, Account
import secrets


@dataclass
class AutomationData:
    credentials: Account = None
    message_obj: List[MessageObject] = field(default_factory=list)
    check_messaged_before: bool = False
    table_data: List = field(default_factory=list)
    headless: bool = False

    def make_message_obj(self, addressee_set_name: str, message_set_name: str):
        # delete any existing message objects
        self.message_obj = []
        addressee_set = get_addressee_set_for_set_name(addressee_set_name, names_only=True)
        message_set = get_messages_for_set_name(message_set_name)

        # split messages and addressees into sets with names and no names
        no_name_addr = list(filter(lambda a: a[1] is None, addressee_set))
        name_addr = [a for a in addressee_set if a not in no_name_addr]
        no_name_msg = list(filter(lambda m: '{name}' not in m, message_set))
        name_msg = [m for m in message_set if m not in no_name_msg]

        # add messages without names
        if len(no_name_addr) > 0:
            for a in no_name_addr:
                msg = secrets.choice(no_name_msg)
                self.message_obj.append(MessageObject(msg, a[0]))

        # add messages with names
        if len(name_addr) > 0:
            for a in name_addr:
                if len(name_msg) > 0:
                    msg = secrets.choice(name_msg)
                    self.message_obj.append(MessageObject(msg.format(name=a[1]), a[0], a[1]))
                else:
                    msg = secrets.choice(no_name_msg)
                    self.message_obj.append(MessageObject(msg, a[0]))

        # create the table data
        self.table_data = [[a.addressee, a.name, a.text] for a in self.message_obj]
