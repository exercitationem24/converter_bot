from requests import get
from decouple import config
from settings import API_URL, CURRRENCIES
import json


class APIException(Exception):
    """Класс ошибки, обрабатывающей неправильный ввод и ошибки на стороне API"""
    pass


class CurrensyConverter:
    """Класс конкертера валют"""
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        """Метод для перевода валюты"""
        apikey = config("API_KEY", default="NOT_FOUND")
        base, quote = base.upper(), quote.upper()
        if base not in CURRRENCIES.values() and base.lower() not in CURRRENCIES.keys():
            raise APIException("Валюта base отсутствует в списке допустимых валют!")
        if quote not in CURRRENCIES.values() and quote.lower() not in CURRRENCIES.keys():
            raise APIException("Валюта quote отсутствует в списке допустимых валют!")
        base = CURRRENCIES.get(base.lower(), base)
        quote = CURRRENCIES.get(quote.lower(), quote)
        if base == quote:
            raise APIException("Нельзя переводить из одной валюты в точно такую же!")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Сумма для перевода не является числом!")
        if amount < 0:
            raise APIException("Вы пытаетесь перевести отрицательное число валюты!")
        responce = get(API_URL, params={"apikey": apikey, "base_currency": base, "currencies": quote})
        data = json.loads(responce.content)
        return round(data["data"][quote] * amount, 4)