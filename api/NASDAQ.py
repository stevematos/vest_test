import requests


class NASDAQ:
    def __init__(self):
        self._url_base = 'https://api.nasdaq.com/api'
        self._headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

    def get_data_for_symbol(self, symbol: str):
        url_format = f'{self._url_base}/quote/{symbol}/info?assetclass=stocks'
        response = requests.get(url_format, headers=self._headers)
        return response.json()


