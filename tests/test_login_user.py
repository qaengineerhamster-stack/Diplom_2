import allure

from data import LOGIN_INVALID_CREDENTIALS_MESSAGE
from helpers import login_user


@allure.suite("Логин пользователя")
class TestLoginUser:

    # Проверяет только успешный вход под существующим пользователем.
    def test_login_existing_user_success(self, registered_user):
        response = login_user(registered_user["user_data"])

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

    # Проверяет только ошибку входа с неверным логином и паролем.
    def test_login_with_invalid_login_and_password_returns_error(self):
        invalid_data = {
            "email": "wrong_email@mail.com",
            "password": "wrongpassword"
        }

        response = login_user(invalid_data)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == LOGIN_INVALID_CREDENTIALS_MESSAGE