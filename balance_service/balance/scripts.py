from forex_python.converter import CurrencyRates

from balance.errors import CurrencyNotFound, ErrorResponse


CURRENCIES = ["USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK",
    "CHF", "ISK", "NOK", "HRK", "RUB", "TRY", "AUD", "BRL", "CAD", "CNY", "HKD",
    "IDR", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR"]

def convert(currency, amount):
    if currency not in CURRENCIES:
        raise CurrencyNotFound
    client = CurrencyRates(force_decimal=True)
    converted_balance = client.convert('RUB', currency, amount)    
    return converted_balance
