import allure
import requests

from data import generate_user_data, INVALID_INGREDIENT_HASHES
from helpers import create_user, login_user, delete_user, get_ingredient_ids
from urls import ORDERS_URL


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth_success(self):
        user_data = generate_user_data()
        create_response = create_user(user_data)
        assert create_response.status_code == 200

        login_response = login_user(user_data)
        access_token = login_response.json()["accessToken"]

        order_data = {
            "ingredients": get_ingredient_ids()
        }

        response = requests.post(
            ORDERS_URL,
            json=order_data,
            headers={"Authorization": access_token}
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "name" in response.json()
        assert "order" in response.json()

        delete_user(access_token)

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_success(self):
        order_data = {
            "ingredients": get_ingredient_ids()
        }

        response = requests.post(ORDERS_URL, json=order_data)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "name" in response.json()
        assert "order" in response.json()

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients_success(self):
        order_data = {
            "ingredients": get_ingredient_ids()
        }

        response = requests.post(ORDERS_URL, json=order_data)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_returns_error(self):
        order_data = {
            "ingredients": []
        }

        response = requests.post(ORDERS_URL, json=order_data)

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_hash_returns_error(self):
        order_data = {
            "ingredients": INVALID_INGREDIENT_HASHES
        }

        response = requests.post(ORDERS_URL, json=order_data)

        assert response.status_code == 500