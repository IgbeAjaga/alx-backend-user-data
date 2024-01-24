#!/usr/bin/env python3
"""
Module for end-to-end integration tests using the requests module.
"""
import requests

BASE_URL = "http://127.0.0.1:5000"

def register_user(email: str, password: str) -> None:
    """
    Registers a user by making a POST request to the /users endpoint.

    Args:
        email (str): Email address of the user.
        password (str): Password for the user.

    Returns:
        None
    """
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print("User registered successfully.")

def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempts to log in with wrong password and validates the expected response

    Args:
        email (str): Email address of the user.
        password (str): Incorrect password.

    Returns:
        None
    """
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401
    print("Login with wrong password failed as expected.")

def log_in(email: str, password: str) -> str:
    """
    Logs in a user by making a POST request to the /sessions endpoint.

    Args:
        email (str): Email address of the user.
        password (str): Password for the user.

    Returns:
        str: Session ID obtained after successful login.
    """
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print("Login successful.")
    return response.cookies.get("session_id")

def profile_unlogged() -> None:
    """
    Attempts to access the user profile without logging in and validates the expected response.

    Returns:
        None
    """
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403
    print("Profile access without login failed as expected.")

def profile_logged(session_id: str) -> None:
    """
    Accesses the user profile after logging in and validates the expected response.

    Args:
        session_id (str): Session ID obtained after successful login.

    Returns:
        None
    """
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    print("Profile access with login successful.")

def log_out(session_id: str) -> None:
    """
    Logs out a user by making a DELETE request to the /sessions endpoint.

    Args:
        session_id (str): Session ID obtained after successful login.

    Returns:
        None
    """
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    print("Logout successful.")

def reset_password_token(email: str) -> str:
    """
    Requests a password reset token by making a POST request to the /reset_password endpoint.

    Args:
        email (str): Email address of the user.

    Returns:
        str: Password reset token obtained after the request.
    """
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print("Password reset token generated.")
    return response.json()["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the user's password using a reset token by making a PUT request

    Args:
        email (str): Email address of the user.
        reset_token (str): Password reset token.
        new_password (str): New password to set.

    Returns:
        None
    """
    url = f"{BASE_URL}/reset_password"
    data = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200
    print("Password updated successfully.")

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
