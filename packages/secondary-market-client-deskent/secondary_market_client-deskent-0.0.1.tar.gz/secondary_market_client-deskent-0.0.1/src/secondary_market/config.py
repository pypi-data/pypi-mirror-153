# аукцион для прогрева
lot_id = 27674529

# Количество запросов для каждого продукта (не больше 500)
requestsNumber = 500

# Время окончания аукциона
saleTime: dict = {
    "year": 2022,
    "month": 5,
    "day": 27,
    "hour": 15,
    "minute": 33,
    "second": 0,
}

currency: str = "BUSD"

product_data: list = [
    {
        "productId": 1234567,
        'amount': 1,
        'tradeType': 0,
        'proxy': '111.111.111.111:1111',
    },
]

# логин и пароль от проксей
proxy_login = 'ТВОЙ_ПРОКСИ_ЮЗЕР'
proxy_password = 'ПАРОЛЬ ОТ ПРОКСИ'
