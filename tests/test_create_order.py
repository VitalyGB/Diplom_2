import requests
import allure

from data.ingredients import Ingredients
from data.text_response import TextResponse
from data.urls import URL, Endpoints
from data.status_code import StatusCode


class TestCreateOrder:

    @allure.title('Проверка создания заказа авторизованным пользователем')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на создание заказа с авторизацией;
                        3. Проверяем ответ;
                        4. Удаляем пользователя.
                        ''')
    def test_create_order_whith_auth(self, create_new_user):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers, data=Ingredients.correct_ingredients_data)
        assert response.status_code == StatusCode.OK and response.json().get("success") == True

    @allure.title('Проверка создания заказа без авторизации')
    @allure.description('''
                        1. Отправляем запрос на создание заказа без авторизации;
                        2. Проверяем ответ;
                        ''')
    def test_create_order_without_auth(self):
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, data=Ingredients.correct_ingredients_data)
        assert response.status_code == StatusCode.OK and response.json().get("success") == True

    @allure.title('Проверка создания заказа авторизованным пользователем без передачи ингредиентов')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на создание заказа без передачи ID ингредиентов с авторизацией;
                        3. Проверяем ответ;
                        4. Удаляем пользователя.
                        ''')
    def test_create_order_whithout_ingredients(self, create_new_user):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers, data=Ingredients.incorrect_ingredients_data_without_filling)
        assert response.status_code == StatusCode.BAD_REQUEST and response.json().get("success") == False

    @allure.title('Проверка создания заказа авторизованным пользователем с невалидным хэшем')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на создание заказа с невалидным ID ингредиентов с авторизацией;
                        3. Проверяем ответ;
                        4. Удаляем пользователя.
                        ''')
    def test_create_order_incorrect_hash(self, create_new_user):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers, data=Ingredients.incorrect_ingredients_data_hash)
        assert response.status_code == StatusCode.INTERNAL_SERVER_ERROR and TextResponse.SERVER_ERROR in response.text