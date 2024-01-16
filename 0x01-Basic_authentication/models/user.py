#!/usr/bin/env python3
""" User module for models
"""


from models.base import Base
import hashlib


class User(Base):
    """ User class for models
    """
    def __init__(self):
        """ Initialize user model
        """
        super().__init__()
        self.email = ''
        self.first_name = ''
        self.last_name = ''
        self.password = ''

    def is_valid_password(self, pwd: str) -> bool:
        """ Check if password is valid
        """
        return hashlib.md5(pwd.encode()).hexdigest() == self.password

    def display_name(self) -> str:
        """ Get user's display name
        """
        return '{} {}'.format(self.first_name, self.last_name)
