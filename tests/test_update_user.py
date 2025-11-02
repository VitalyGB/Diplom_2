import pytest
import requests
import allure

from data.text_response import TextResponse
from helpers.helpers import Person
from data.status_code import StatusCode
from data.urls import URL, Endpoints


class TestChangeUserData:

    @allure.title('Проверка изменения данных с авторизацией')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на изменение параметров пользователя;
                        3. Проверяем ответ;
                        3. Удаляем пользователя.
                        ''')
    @pytest.mark.parametrize('data', [
        Person.create_data_correct_user()["name"],
        Person.create_data_correct_user()["password"],
        Person.create_data_correct_user()["email"]
    ])
    def test_change_person_data(self, create_new_user, data):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.patch(URL.main_url + Endpoints.DATA_CHANGE, headers=headers, data=data)
        assert response.status_code == StatusCode.OK and response.json().get("success") == True

    @allure.title('Проверка изменения данных пользователя без авторизации')
    @allure.description('''
                        1. Отправляем запрос на изменение параметров пользователя;
                        2. Проверяем ответ.
                        ''')
    @pytest.mark.parametrize('data', [
        Person.create_data_correct_user()["name"],
        Person.create_data_correct_user()["password"],
        Person.create_data_correct_user()["email"]
    ])
    def test_change_person_data_whithout_auth(self, data):
        response = requests.patch(URL.main_url + Endpoints.DATA_CHANGE, data=data)
        assert response.status_code == StatusCode.UNAUTHORIZED and (
            response.json().get("message") == TextResponse.UNAUTHORIZED
            )