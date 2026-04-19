import allure

from data import REQUIRED_FIELDS_MESSAGE, USER_ALREADY_EXISTS_MESSAGE
from helpers import create_user, delete_user, generate_user_data, login_user


@allure.suite("Создание пользователя")
class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self):
        user_data = generate_user_data()
        access_token = None

        try:
            response = create_user(user_data)

            assert response.status_code == 200
            assert response.json()["success"] is True

            login_response = login_user(user_data)
            access_token = login_response.json().get("accessToken")
        finally:
            if access_token:
                delete_user(access_token)

    @allure.title("Создание уже существующего пользователя возвращает ошибку")
    def test_create_existing_user_returns_error(self):
        user_data = generate_user_data()
        access_token = None

        try:
            first_response = create_user(user_data)
            assert first_response.status_code == 200

            login_response = login_user(user_data)
            access_token = login_response.json().get("accessToken")

            second_response = create_user(user_data)

            assert second_response.status_code == 403
            assert second_response.json()["success"] is False
            assert second_response.json()["message"] == USER_ALREADY_EXISTS_MESSAGE
        finally:
            if access_token:
                delete_user(access_token)

    @allure.title("Создание пользователя без обязательного поля возвращает ошибку")
    def test_create_user_without_required_field_returns_error(self):
        user_data = generate_user_data()
        incomplete_user_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }

        response = create_user(incomplete_user_data)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == REQUIRED_FIELDS_MESSAGE