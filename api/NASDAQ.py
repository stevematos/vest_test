import requests


class NASDAQ:
    def __init__(self):
        self._url_format = 'https://api.nasdaq.com/api/quote/{}/info?assetclass=stocks'
        self._headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

    def get_data_for_symbol(self, symbol: str):
        response = requests.get(self._url_format.format(symbol), headers=self._headers)
        print(response.status_code)
        return response.json()


