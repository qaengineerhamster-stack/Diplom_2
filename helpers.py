import random
import string

import allure
import requests

from data import USER_PASSWORD
from urls import LOGIN_URL, ORDERS_URL, REGISTER_URL, USER_URL


@allure.step("Сгенерировать данные пользователя")
def generate_user_data():
    random_string = "".join(random.choices(string.ascii_lowercase, k=8))
    return {
        "email": f"test_{random_string}@mail.com",
        "password": USER_PASSWORD,
        "name": f"name_{random_string}",
    }


@allure.step("Создать пользователя")
def create_user(user_data):
    return requests.post(REGISTER_URL, json=user_data)


@allure.step("Логин пользователя")
def login_user(user_data):
    return requests.post(
        LOGIN_URL,
        json={
            "email": user_data["email"],
            "password": user_data["password"],
        },
    )


@allure.step("Удалить пользователя")
def delete_user(access_token):
    return requests.delete(USER_URL, headers={"Authorization": access_token})


@allure.step("Создать заказ")
def create_order(ingredients, access_token=None):
    headers = {}
    if access_token:
        headers["Authorization"] = access_token

    return requests.post(ORDERS_URL, json={"ingredients": ingredients}, headers=headers)
