from dataclasses import dataclass, field
from typing import List


@dataclass
class Account:
    username: str = None
    password: str = None
    session: List = field(default_factory=list)

    def make_new(self, username, password, session=None):
        self.username = username
        self.password = password
        if session is not None:
            self.session = session
@dataclass
class Message:
    text: str
    
@dataclass
class Addressee:
    username: str
    name: str = None
    
@dataclass
class MessageObject:
    text: str
    addressee: str
    name: str = None