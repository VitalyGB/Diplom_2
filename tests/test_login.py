import allure
import requests

from helpers.helpers import Person
from data.status_code import StatusCode
from data.urls import URL, Endpoints


class TestCreateUser:

    @allure.title('Проверка логин под существующим пользователем')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на логин в системе;
                        3. Проверяем ответ;
                        3. Удаляем пользователя.
                        ''')
    def test_login_user(self, create_new_user):
        response = create_new_user
        login = requests.post(URL.main_url + Endpoints.LOGIN, data=response[0])
        assert login.status_code == StatusCode.OK and login.json().get("success") == True

    @allure.title('Проверка логин под несуществующим пользователем')
    @allure.description('''
                        1. Отправляем запрос на логин в системе без регистрации;
                        2. Проверяем ответ.
                        ''')
    def test_login_under_none_user(self):
        login = requests.post(URL.main_url + Endpoints.LOGIN, data=Person.create_data_incorrect_user_without_name())
        assert login.status_code == StatusCode.UNAUTHORIZED and login.json().get("success") == False