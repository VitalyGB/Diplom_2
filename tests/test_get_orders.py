import requests
import allure

from data.ingredients import Ingredients
from data.status_code import StatusCode
from data.text_response import TextResponse
from data.urls import URL, Endpoints


class TestCreateOrder:

    @allure.title('Проверка создания заказа авторизованным пользователем')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на создание заказа;
                        3. Отправляем запрос на получение заказа пользователя
                        4. Проверяем ответ;
                        5. Удаляем пользователя
                        ''')
    def test_get_order_whith_auth(self, create_new_user):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response_create_order = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers, data=Ingredients.correct_ingredients_data)
        response_get_order = requests.get(URL.main_url + Endpoints.GET_ORDERS, headers=headers)
        assert response_get_order.status_code == StatusCode.OK and (
            response_create_order.json()["order"]["number"] == response_get_order.json()["orders"][0]["number"]
            )

    @allure.title('Проверка получения заказа неавторизованным пользователем')
    @allure.description('''
                        1. Отправляем запрос на получение заказа;
                        2. Проверяем ответ.
                        ''')
    def test_get_order_whithout_auth(self):
        response_get_order = requests.get(URL.main_url + Endpoints.GET_ORDERS)
        assert response_get_order.status_code == StatusCode.UNAUTHORIZED and (
            TextResponse.UNAUTHORIZED in response_get_order.text
            )