
#!/usr/bin/env python3
""" End-to-end integration test
"""
import requests

URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """test register user

    Args:
        email (str): _description_
        password (str): _description_
    """
    data = {"email": email, "password": password}
    res = requests.post(f"{URL}/users", data=data)
    payload = {"email": email, "message": "user created"}

    assert res.status_code == 200
    assert res.json() == payload


def log_in_wrong_password(email: str, password: str) -> None:
    """test login wrong credentials

    Args:
        email (str): _description_
        password (str): _description_
    """
    data = {"email": email, "password": password}
    res = requests.post(f"{URL}/sessions", data=data)

    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """test login

    Args:
        email (str): _description_
        password (str): _description_

    Returns:
        str: _description_
    """
    data = {"email": email, "password": password}
    res = requests.post(f"{URL}/sessions", data=data)
    payload = {"email": email, "message": "logged in"}

    assert res.status_code == 200
    assert res.json() == payload

    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test view profile unauthenticated"""
    cookies = dict(session_id=None)
    res = requests.get(f"{URL}/profile", cookies=cookies)

    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test view profile authenticated

    Args:
        session_id (str): _description_
    """
    cookies = dict(session_id=session_id)
    res = requests.get(f"{URL}/profile", cookies=cookies)

    assert res.status_code == 200


def log_out(session_id: str) -> None:
    """Test logout

    Args:
        session_id (str): _description_
    """
    cookies = dict(session_id=session_id)
    res = requests.delete(f"{URL}/sessions",
                          cookies=cookies,
                          allow_redirects=True)

    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """Test reset password

    Args:
        email (str): _description_

    Returns:
        str: _description_
    """
    data = {"email": email}
    res = requests.post(f"{URL}/reset_password", data=data)
    reset_token = dict(res.json()).get("reset_token")

    assert res.status_code == 200

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update user password

    Args:
        email (str): _description_
        reset_token (str): _description_
        new_password (str): _description_
    """
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    res = requests.put(f"{URL}/reset_password", data=data)

    assert res.status_code == 200


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

