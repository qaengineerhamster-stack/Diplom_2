import allure

from data import get_user_without_field
from helpers import create_user


class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, user_data, cleanup_user):
        response = create_user(user_data)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user_returns_error(self, registered_user):
        response = create_user(registered_user["user_data"])

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "User already exists"

    @allure.title("Создание пользователя без одного обязательного поля")
    def test_create_user_without_required_field_returns_error(self):
        user_data = get_user_without_field("name")

        response = create_user(user_data)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "Email, password and name are required fields"