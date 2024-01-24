#!/usr/bin/env python3
"""
Database module for the authentication service.
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from user import Base


class DB:
    """DB class for interacting with the database."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """Add a new user to the database."""
        pass

    def find_user_by(self, **kwargs):
        """Find a user by the specified criteria."""
        pass

    def update_user(self, user_id, **kwargs):
        """Update user information in the database."""
        pass
