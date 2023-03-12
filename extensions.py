import requests
import json
from config import keys

class ConversionException(Exception):
    pass


class CurrencyExchanger:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Unable to process currency {quote}, please review the available currencies here /values')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Unable to process currency {base}, please review the available currencies here /values')
        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Unable to process quantity {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base