from dataclasses import dataclass, field
from typing import List


@dataclass
class Account:
    username: str = None
    password: str = None
    session: List = field(default_factory=list)
    last_user_messaged = None

    def make_new(self, username, password, session=None):
        self.username = username
        self.password = password
        if session is not None:
            self.session = session
