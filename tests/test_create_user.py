import pytest
import allure
import requests

from data.text_response import TextResponse
from helpers.helpers import Person
from data.status_code import StatusCode
from data.urls import URL, Endpoints

class TestCreateUser:

    @allure.title('Проверка создания уникального пользователя')
    @allure.description(
        '''
        1. Отправляем запрос на создание пользователя;
        2. Проверяем ответ;
        3. Удаляем пользователя.
        '''
    )
    def test_create_user(self):
        with allure.step("Создание уникального пользователя"):
            payload = Person.create_data_correct_user()
            response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
        with allure.step("Проверка успешного создания пользователя"):
            assert response.json().get("success") is True and response.status_code == StatusCode.OK
        with allure.step("Удаление пользователя"):
            token = response.json()["accessToken"]
            requests.delete(URL.main_url + Endpoints.DELETE_USER, headers={"Authorization": token})

    @allure.title('Проверка создания дублирующего пользователя')
    @allure.description(
        '''
        1. Отправляем запрос на создание пользователя;
        2. Получаем данные для регистрации;
        3. Отправляем повторный запрос на создание пользователя;
        4. Проверяем ответ;
        5. Удаляем пользователя.
        '''
    )
    def test_create_double_user(self):
        with allure.step("Создание пользователя"):
            payload = Person.create_data_correct_user()
            response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
        with allure.step("Повторная попытка регистрации пользователя"):
            response_double_register = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
        with allure.step("Проверка ответа на повторную регистрацию"):
            assert response_double_register.status_code == StatusCode.FORBIDDEN and (
                response_double_register.json().get("message") == TextResponse.CREATE_DOUBLE_USER
            )
        with allure.step("Удаление пользователя"):
            token = response.json()["accessToken"]
            requests.delete(URL.main_url + Endpoints.DELETE_USER, headers={"Authorization": token})

    @allure.title('Проверка создания некорректного пользователя')
    @allure.description(
        '''
        1. Отправляем запрос на создание пользователя с некорректными данными;
        2. Проверяем ответ.
        '''
    )
    @pytest.mark.parametrize(
        'payload',
        [
            Person.create_data_incorrect_user_without_email(),
            Person.create_data_incorrect_user_without_name(),
            Person.create_data_incorrect_user_without_password()
        ]
    )
    def test_create_user_incorrect_data(self, payload):
        with allure.step("Создание пользователя с некорректными данными"):
            response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
        with allure.step("Проверка ответа на некорректные данные"):
            assert response.status_code == StatusCode.FORBIDDEN and response.json().get("success") is False
