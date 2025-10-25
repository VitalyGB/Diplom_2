class URL:
    """URL сервиса"""

    main_url = 'https://stellarburgers.education-services.ru/'


class Endpoints:
    """Ручки для работы с API"""

    CREATE_USER = '/api/auth/register'
    LOGIN = '/api/auth/login'
    DELETE_USER = '/api/auth/user'
    CREATE_ORDER = '/api/orders'
    GET_ORDERS = '/api/orders'
    DATA_CHANGE = '/api/auth/user'