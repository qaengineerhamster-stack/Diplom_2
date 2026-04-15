import allure

from data import generate_user_data, INVALID_LOGIN_DATA
from helpers import create_user, login_user, delete_user


class TestLoginUser:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(self):
        user_data = generate_user_data()
        create_response = create_user(user_data)

        assert create_response.status_code == 200

        login_response = login_user(user_data)

        assert login_response.status_code == 200
        assert login_response.json()["success"] is True
        assert "accessToken" in login_response.json()

        access_token = login_response.json()["accessToken"]
        delete_user(access_token)

    @allure.title("Вход с неверным логином и паролем")
    def test_login_with_invalid_credentials_returns_error(self):
        response = login_user(INVALID_LOGIN_DATA)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "email or password are incorrect"