import random
import string


def generate_user_data():
    suffix = ''.join(random.choices(string.ascii_lowercase, k=8))
    return {
        "email": f"test_{suffix}@mail.com",
        "password": "123456",
        "name": f"name_{suffix}"
    }


INVALID_LOGIN_DATA = {
    "email": "wrong_user@mail.com",
    "password": "wrong_password"
}


def get_user_without_field(field_name):
    user_data = generate_user_data()
    user_data.pop(field_name)
    return user_data


INVALID_INGREDIENT_HASHES = ["invalid_hash_12345"]