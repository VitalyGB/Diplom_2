import pytest
import allure
import requests

from data.text_response import TextResponse
from helpers.helpers import Person
from data.status_code import StatusCode
from data.urls import URL, Endpoints


class TestCreateUser:

    @allure.title('Проверка создания уникального пользователя')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Проверяем ответ;
                        3. Удаляем пользователя.
                        ''')
    def test_create_user(self, create_new_user):
        response = create_new_user
        assert response[1].json().get("success") == True and response[1].status_code == StatusCode.OK

    @allure.title('Проверка создания дублирующего пользователя')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Получаем данные для регистрации;
                        3. Отправляем повторный запрос на создание пользователя;
                        4. Проверяем ответ;
                        5. Удаляем пользователя.
                        ''')
    def test_create_double_user(self, create_new_user):
        response = create_new_user
        payload = response[0]
        response_double_register = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
        assert response_double_register.status_code == StatusCode.FORBIDDEN and (
            response_double_register.json().get("message") == TextResponse.CREATE_DOUBLE_USER
            )

    @allure.title('Проверка создания некорректного пользователя')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя с некорректными данными;
                        2. Проверяем ответ.
                        ''')
    @pytest.mark.parametrize('payload', [
        Person.create_data_incorrect_user_without_email(),
        Person.create_data_incorrect_user_without_name(),
        Person.create_data_incorrect_user_without_password()
    ])
    def test_create_user_incorrect_data(self, payload):
        response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
        assert response.status_code == StatusCode.FORBIDDEN and response.json().get("success") == False