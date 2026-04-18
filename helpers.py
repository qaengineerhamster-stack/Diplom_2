import allure
import requests

from urls import REGISTER_URL, LOGIN_URL, USER_URL, INGREDIENTS_URL, ORDERS_URL


@allure.step("Создать пользователя")
def create_user(user_data):
    return requests.post(REGISTER_URL, json=user_data)


@allure.step("Авторизовать пользователя")
def login_user(user_data):
    return requests.post(
        LOGIN_URL,
        json={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )


@allure.step("Удалить пользователя")
def delete_user(access_token):
    return requests.delete(
        USER_URL,
        headers={"Authorization": access_token}
    )


@allure.step("Получить список ингредиентов")
def get_ingredients():
    response = requests.get(INGREDIENTS_URL)
    return response.json()["data"]


@allure.step("Получить id ингредиентов")
def get_ingredient_ids(count=2):
    ingredients = get_ingredients()
    return [ingredient["_id"] for ingredient in ingredients[:count]]


@allure.step("Создать заказ")
def create_order(ingredients, access_token=None):
    headers = {}
    if access_token:
        headers["Authorization"] = access_token

    return requests.post(
        ORDERS_URL,
        json={"ingredients": ingredients},
        headers=headers
    )