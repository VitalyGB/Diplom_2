from faker import Faker


class Person:
    """Методы генерации данных для регистрации"""

    @staticmethod
    def create_data_correct_user():
        faker = Faker('ru_RU')
        data = {
            "email": faker.email(),
            "password": faker.password(),
            "name": faker.first_name()
        }
        return data

    @staticmethod
    def create_data_incorrect_user_without_email():
        faker = Faker('ru_RU')
        data = {
            "password": faker.password(),
            "name": faker.first_name()
        }
        return data

    @staticmethod
    def create_data_incorrect_user_without_password():
        faker = Faker('ru_RU')
        data = {
            "email": faker.email(),
            "name": faker.first_name()
        }
        return data

    @staticmethod
    def create_data_incorrect_user_without_name():
        faker = Faker('ru_RU')
        data = {
            "email": faker.email(),
            "password": faker.password(),
        }
        return data
