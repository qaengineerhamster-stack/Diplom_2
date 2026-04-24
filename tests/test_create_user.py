import allure

from data import REQUIRED_FIELDS_MESSAGE, USER_ALREADY_EXISTS_MESSAGE
from helpers import create_user, generate_user_data


@allure.suite("Создание пользователя")
class TestCreateUser:

    # Проверяет только успешное создание уникального пользователя.
    def test_create_unique_user_success(self, users_for_cleanup):
        user_data = generate_user_data()
        users_for_cleanup.append(user_data)

        response = create_user(user_data)

        assert response.status_code == 200
        assert response.json()["success"] is True

    # Проверяет только ошибку при создании пользователя, который уже зарегистрирован.
    def test_create_existing_user_returns_error(self, users_for_cleanup):
        user_data = generate_user_data()
        users_for_cleanup.append(user_data)

        create_user(user_data)
        second_response = create_user(user_data)

        assert second_response.status_code == 403
        assert second_response.json()["success"] is False
        assert second_response.json()["message"] == USER_ALREADY_EXISTS_MESSAGE

    # Проверяет только ошибку при создании пользователя без одного обязательного поля.
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