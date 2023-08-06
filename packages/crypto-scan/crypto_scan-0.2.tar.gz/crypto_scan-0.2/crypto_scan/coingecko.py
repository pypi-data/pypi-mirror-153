import requests
import pandas as pd

# https://www.coingecko.com/en/api/documentation


class CoinGecko:

    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3"
        # default parameters
        self.default_parameters = {
        }

    def get_params(self, **kwargs):
        return {**self.default_parameters, **kwargs}

    def get_coins(self):
        url = f"{self.url}/coins/list"
        r = requests.get(url)
        return pd.DataFrame(r.json())

    def get_coin_history(self, coin_id, date):
        url = f"{self.url}/coins/{coin_id}/history"
        params = {
            "date": date,
            "localization": False,
        }
        r = requests.get(url, params=self.get_params(**params))
        return r.json()

    def get_coin_by_chain_contract(self, chain, contract_addr):
        url = f"{self.url}/coins/{chain}/contract/{contract_addr}"
        r = requests.get(url)
        return r.json()

    def get_coin_market_inusd_by_chain_contract(self, chain, contract_addr, days_back='max'):
        url = f"{self.url}/coins/{chain}/contract/{contract_addr}/market_chart"
        params = {
            "vs_currency": 'usd',
            "days": days_back,
        }
        r = requests.get(url, params=self.get_params(**params))
        return r.json()
