import requests

from urls import REGISTER_URL, LOGIN_URL, USER_URL, INGREDIENTS_URL


def create_user(user_data):
    return requests.post(REGISTER_URL, json=user_data)


def login_user(user_data):
    return requests.post(
        LOGIN_URL,
        json={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )


def delete_user(access_token):
    return requests.delete(
        USER_URL,
        headers={"Authorization": access_token}
    )


def get_ingredients():
    response = requests.get(INGREDIENTS_URL)
    return response.json()["data"]


def get_ingredient_ids(count=2):
    ingredients = get_ingredients()
    return [ingredient["_id"] for ingredient in ingredients[:count]]