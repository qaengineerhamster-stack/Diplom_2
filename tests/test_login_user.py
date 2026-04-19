import allure

from data import LOGIN_INVALID_CREDENTIALS_MESSAGE
from helpers import create_user, delete_user, generate_user_data, login_user


@allure.suite("Логин пользователя")
class TestLoginUser:
    @allure.title("Успешный логин существующего пользователя")
    def test_login_existing_user_success(self, registered_user):
        response = login_user(registered_user["user_data"])

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

    @allure.title("Логин с неверными данными возвращает ошибку")
    def test_login_with_invalid_credentials_returns_error(self):
        user_data = generate_user_data()
        access_token = None

        try:
            create_response = create_user(user_data)
            assert create_response.status_code == 200

            login_response = login_user(user_data)
            access_token = login_response.json().get("accessToken")

            invalid_data = {
                "email": user_data["email"],
                "password": "wrongpassword"
            }

            response = login_user(invalid_data)

            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == LOGIN_INVALID_CREDENTIALS_MESSAGE
        finally:
            if access_token:
                delete_user(access_token)