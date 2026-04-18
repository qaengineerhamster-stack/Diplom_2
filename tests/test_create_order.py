import allure

from data import INVALID_INGREDIENT_HASHES
from helpers import create_order, get_ingredient_ids


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth_success(self, registered_user):
        response = create_order(
            ingredients=get_ingredient_ids(),
            access_token=registered_user["access_token"]
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "name" in response.json()
        assert "order" in response.json()

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_success(self):
        response = create_order(
            ingredients=get_ingredient_ids()
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "name" in response.json()
        assert "order" in response.json()

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients_success(self):
        response = create_order(
            ingredients=get_ingredient_ids()
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_returns_error(self):
        response = create_order(ingredients=[])

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_hash_returns_error(self):
        response = create_order(
            ingredients=INVALID_INGREDIENT_HASHES
        )

        assert response.status_code == 500