import allure

from data import INVALID_LOGIN_DATA
from helpers import login_user


class TestLoginUser:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(self, registered_user):
        response = login_user(registered_user["user_data"])

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Вход с неверным логином и паролем")
    def test_login_with_invalid_credentials_returns_error(self):
        response = login_user(INVALID_LOGIN_DATA)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "email or password are incorrect"