#!/usr/bin/env python3
"""Auth module.
"""
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm.exc import MultipleResultsFound
from user import User, Base
from db import DB
from typing import Union


def get_user(email: str) -> Union[User, None]:
    """
    Function that returns a user instance based on email.
    """
    db = DB()
    try:
        user = db.find_user_by(email=email)
        return user
    except NoResultFound:
        return None


def register_user(email: str, hashed_password: str) -> Union[User, str]:
    """
    Function that registers a new user and returns the user instance.
    """
    db = DB()
    try:
        user = db.add_user(email=email, hashed_password=hashed_password)
        return user
    except IntegrityError:
        return "User with this email already exists."


def valid_login(email: str, password: str) -> Union[User, str]:
    """
    Function that validates login credentials and returns the user instance.
    """
    user = get_user(email)
    if user and user.verify_password(password):
        return user
    return "Invalid email or password"


def create_user(email: str, password: str) -> Union[User, str]:
    """
    Function that creates a new user and returns the user instance.
    """
    hashed_password = User.hash_password(password)
    return register_user(email, hashed_password)


def get_user_by_id(user_id: int) -> Union[User, None]:
    """
    Function that returns a user instance based on user_id.
    """
    db = DB()
    try:
        user = db.find_user_by(id=user_id)
        return user
    except NoResultFound:
        return None


def update_password(
        user_id: int, current_password: str, new_password: str) -> Union[
                User, str]:
    """
    Function that updates the user's password and returns the user instance.
    """
    user = get_user_by_id(user_id)
    if user and user.verify_password(current_password):
        db = DB()
        hashed_password = User.hash_password(new_password)
        db.update_user(user_id, hashed_password=hashed_password)
        return get_user_by_id(user_id)
    return "Invalid current password"
