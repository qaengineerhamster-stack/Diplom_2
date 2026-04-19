import allure

from data import (
    ORDER_INGREDIENTS_REQUIRED_MESSAGE,
    ORDER_INVALID_HASH_MESSAGE,
)
from helpers import create_order, create_user, delete_user, generate_user_data, login_user


@allure.suite("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth_success(self):
        user_data = generate_user_data()
        access_token = None

        try:
            create_response = create_user(user_data)
            assert create_response.status_code == 200

            login_response = login_user(user_data)
            access_token = login_response.json().get("accessToken")

            ingredients = [
                "61c0c5a71d1f82001bdaaa6d",
                "61c0c5a71d1f82001bdaaa6f"
            ]

            response = create_order(ingredients, access_token)

            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "number" in response.json()["order"]
        finally:
            if access_token:
                delete_user(access_token)

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_success(self):
        ingredients = [
            "61c0c5a71d1f82001bdaaa6d",
            "61c0c5a71d1f82001bdaaa6f"
        ]

        response = create_order(ingredients)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "number" in response.json()["order"]

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients_success(self):
        ingredients = [
            "61c0c5a71d1f82001bdaaa6d",
            "61c0c5a71d1f82001bdaaa6f"
        ]

        response = create_order(ingredients)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "number" in response.json()["order"]

    @allure.title("Создание заказа без ингредиентов возвращает ошибку")
    def test_create_order_without_ingredients_returns_error(self):
        response = create_order([])

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == ORDER_INGREDIENTS_REQUIRED_MESSAGE

    @allure.title("Создание заказа с неверным хешем ингредиента возвращает ошибку")
    def test_create_order_with_invalid_hash_returns_error(self): 
        response = create_order(["invalid_hash"])

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == ORDER_INVALID_HASH_MESSAGE