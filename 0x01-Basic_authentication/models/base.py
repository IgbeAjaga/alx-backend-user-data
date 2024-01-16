#!/usr/bin/env python3
""" Base module for models
"""


from uuid import uuid4
from datetime import datetime
from typing import TypeVar


class Base:
    """ Base class for models
    """
    def __init__(self):
        """ Initialize base model
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """ Save model to storage
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """ Convert model to dictionary
        """
        d = dict(self.__dict__)
        d['created_at'] = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        d['updated_at'] = self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        return d
