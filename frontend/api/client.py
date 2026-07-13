import requests
import json

BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login/"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register/"


def register():
    data = {
      "email": "string1@email.com",
      "password": "s1234535"
    }
    with requests.Session() as s:
        response = s.post(REGISTER_ENDPOINT, json=data) # , headers={"Authorization": f"Bearer {token}"}

    return response.json()


def login():
    data = {
      "email": "student@example.com",
      "password": "secret123"
    }

    with requests.Session() as s:
        response = s.post(LOGIN_ENDPOINT, json=data) # , headers={"Authorization": f"Bearer {token}"}

    return response.json()


if __name__ == '__main__':
    print(register())
    print(login())