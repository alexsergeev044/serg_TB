import json
import requests
from config import openexchanger_token, exchangerate_token


class APIException (Exception):
    pass


class HTMLException (Exception):
    pass


class CurrencyExcange:
    @staticmethod
    def get_price(val, keys):

        if len(val) != 3:
            raise APIException("Количество параметров должно быть равно трём!")

        quote, base, amount = val

        if quote == base:
            raise APIException("Валюты должны различаться!")

        if quote not in keys.keys():
            raise APIException(f"Некорректное или отсутствующее в базе название валюты '(quote)'!")

        if base not in keys.keys():
            raise APIException(f"Некорректное или отсутствующее в базе название валюты '(base0'!")

        if not amount.isdigit():
            raise APIException("Сумма валюты должна быть положительным числом!")

        if int(amount) <= 0:
            raise APIException("Сумма валюты должна быть положительным числом!")

        result = ""

        try:
            try:
                h = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={openexchanger_token}base=USD&symbols={keys[quote]},{keys[base]}")
                openexrates = round(float(json.loads(h.content)['rates'][keys[base]]) /
                                    float(json.loads(h.content)['rates'][keys[quote]]) * float(amount), 4)
                result += f"По данным openexchangerates.org:\n{amount}{keys[quote]}={openexrates}{keys[base]}\n\n"
            except Exception:
                raise HTMLException(f"Ошибка сервиса openexchangerates.org!\n\n")
        except HTMLException as e:
            result += f"{e}"

        try:
            try:
                e = requests.get(f"http://api.exchangeratesapi.io/v1/latest?"
                                 f"access_key={exchangerate_token}"
                                 f"base=EUR&symbols={keys[quote]},{keys[base]}")
                exratesio = round(float(json.loads(e.content)['rates'][keys[base]]) /
                                  float(json.loads(e.content)['rates'][keys[quote]]) * float(amount), 4)
                result += f"По данным exchangeratesapi.io:\n{amount} {keys[quote]} = {exratesio} {keys[base]}\n\n"
            except Exception:
                raise HTMLException(f"Ошибка сервиса exchangeratesapi.io!/n/n")
        except HTMLException as e:
            result += f"{e}"

        try:
            try:
                r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}")
                cryptocompare = round(float(json.loads(r.content)[keys[base]]) * float(amount), 4)
                result += f"По данным cryptocompare.com:/n" \
                          f"{amount} {keys[quote]} = {cryptocompare} {keys[base]}\n\n"
            except Exception:
                raise HTMLException(f"Ошибка сервиса cryptocompare.com!\n\n")
        except HTMLException as e:
            result += f"{e}"

        return result

