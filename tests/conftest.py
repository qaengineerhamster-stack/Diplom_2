import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from helpers import create_user, delete_user, generate_user_data, login_user


@pytest.fixture
def registered_user():
    user_data = generate_user_data()

    create_user(user_data)
    login_response = login_user(user_data)
    access_token = login_response.json().get("accessToken")

    yield {
        "user_data": user_data,
        "access_token": access_token
    }

    if access_token:
        delete_user(access_token)