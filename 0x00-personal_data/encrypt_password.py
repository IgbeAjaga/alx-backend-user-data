#!/usr/bin/env python3
"""
Password encryption module.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using a random salt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a hashed password matches the provided password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
