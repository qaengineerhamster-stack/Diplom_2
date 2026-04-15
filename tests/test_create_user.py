import allure

from data import generate_user_data, get_user_without_field
from helpers import create_user, login_user, delete_user


class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self):
        user_data = generate_user_data()

        response = create_user(user_data)

        assert response.status_code == 200
        assert response.json()["success"] is True

        login_response = login_user(user_data)
        access_token = login_response.json()["accessToken"]
        delete_user(access_token)

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user_returns_error(self):
        user_data = generate_user_data()

        first_response = create_user(user_data)
        second_response = create_user(user_data)

        assert first_response.status_code == 200
        assert second_response.status_code == 403
        assert second_response.json()["success"] is False
        assert second_response.json()["message"] == "User already exists"

        login_response = login_user(user_data)
        access_token = login_response.json()["accessToken"]
        delete_user(access_token)

    @allure.title("Создание пользователя без одного обязательного поля")
    def test_create_user_without_required_field_returns_error(self):
        user_data = get_user_without_field("name")

        response = create_user(user_data)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "Email, password and name are required fields"