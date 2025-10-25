import pytest
import requests

from helpers.helpers import Person
from data.urls import URL, Endpoints


# Фикстура создания / удаления пользователя
@pytest.fixture
def create_new_user():
    payload = Person.create_data_correct_user()
    response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
    yield payload, response
    token = response.json()["accessToken"]
    requests.delete(URL.main_url + Endpoints.DELETE_USER, headers={"Authorization": token})


# Для корректного отображения аргументов в параметризированном тесте
def pytest_make_parametrize_id(val):
    return repr(val)