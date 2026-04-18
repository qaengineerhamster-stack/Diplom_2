import pytest

from data import generate_user_data
from helpers import create_user, login_user, delete_user


@pytest.fixture
def user_data():
    return generate_user_data()


@pytest.fixture
def cleanup_user(user_data):
    yield
    login_response = login_user(user_data)
    if login_response.status_code == 200 and login_response.json().get("success") is True:
        access_token = login_response.json()["accessToken"]
        delete_user(access_token)


@pytest.fixture
def registered_user():
    user_data = generate_user_data()
    create_response = create_user(user_data)
    assert create_response.status_code == 200
    assert create_response.json()["success"] is True

    login_response = login_user(user_data)
    assert login_response.status_code == 200
    assert login_response.json()["success"] is True

    access_token = login_response.json()["accessToken"]

    yield {
        "user_data": user_data,
        "access_token": access_token
    }

    delete_user(access_token)