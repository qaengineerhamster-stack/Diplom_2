import pytest

from helpers import create_user, delete_user, generate_user_data, login_user


@pytest.fixture
def registered_user():
    user_data = generate_user_data()

    create_user(user_data)
    login_response = login_user(user_data)
    access_token = login_response.json().get("accessToken")

    yield {
        "user_data": user_data,
        "access_token": access_token,
    }

    if access_token:
        delete_user(access_token)


@pytest.fixture
def users_for_cleanup():
    created_users = []

    yield created_users

    for user_data in created_users:
        login_response = login_user(user_data)
        access_token = login_response.json().get("accessToken")

        if access_token:
            delete_user(access_token)
