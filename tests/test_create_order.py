import allure

from data import (
    INVALID_INGREDIENT_HASH,
    ORDER_INGREDIENTS_REQUIRED_MESSAGE,
    VALID_INGREDIENTS,
)
from helpers import create_order


@allure.suite("Создание заказа")
class TestCreateOrder:

    # Проверяет только успешное создание заказа с авторизацией и ингредиентами.
    def test_create_order_with_auth_and_ingredients_success(self, registered_user):
        response = create_order(
            VALID_INGREDIENTS,
            registered_user["access_token"]
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "number" in response.json()["order"]

    # Проверяет только успешное создание заказа без авторизации и с ингредиентами.
    def test_create_order_without_auth_and_ingredients_success(self):
        response = create_order(VALID_INGREDIENTS)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "number" in response.json()["order"]

    # Проверяет только ошибку создания заказа без ингредиентов.
    def test_create_order_without_ingredients_returns_error(self):
        response = create_order([])

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == ORDER_INGREDIENTS_REQUIRED_MESSAGE

    # Проверяет только ошибку создания заказа с неверным хешем ингредиентов.
    # Реальный стенд возвращает 400.
    def test_create_order_with_invalid_hash_returns_error(self):
        response = create_order(INVALID_INGREDIENT_HASH)

        assert response.status_code == 400