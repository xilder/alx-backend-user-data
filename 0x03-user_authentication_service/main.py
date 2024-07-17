#!/usr/bin/env python3
"""
Main file
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """validates the registration function"""
    data = {
        'email': EMAIL,
        'password': PASSWD
    }
    URL = f'{BASE_URL}/users'
    r = requests.post(URL, data=data)
    # assert r.status_code == 200
    # assert r.json() == {'email': EMAIL, 'message': 'user created'}
    r = requests.post(URL, data=data)
    assert r.status_code == 400
    assert r.json() == {'message': 'email already registered'}


def log_in_wrong_password(email: str, password: str) -> None:
    """checks for wrong password"""
    data = {
        'email': EMAIL,
        'password': NEW_PASSWD
    }
    URL = f'{BASE_URL}/sessions'
    r = requests.post(URL, data=data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """test logging behaviour of the app"""
    data = {
        'email': email,
        'password': password
    }
    URL = f'{BASE_URL}/sessions'
    r = requests.post(URL, data=data)
    assert r.status_code == 200
    assert r.json() == {'email': EMAIL, 'message': 'logged in'}
    return r.cookies.get("session_id")


def profile_unlogged() -> None:
    URL = f'{BASE_URL}/profile'
    r = requests.get(URL)
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    URL = f'{BASE_URL}/profile'
    cookie = {
        'session_id': session_id
    }
    r = requests.get(URL, cookies=cookie)
    assert r.json().get('email') == EMAIL
    assert r.status_code == 200


def log_out(session_id: str) -> None:
    """tests the log out route"""
    URL = f'{BASE_URL}/sessions'
    cookie = {
        'session_id': session_id
    }
    r = requests.delete(URL, cookies=cookie)
    assert r.cookies.get('session_id') == None
    assert r.status_code == 200


def reset_password_token(email: str) -> str:
    """tests the reset token route"""
    URL = f'{BASE_URL}/reset_password'


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)