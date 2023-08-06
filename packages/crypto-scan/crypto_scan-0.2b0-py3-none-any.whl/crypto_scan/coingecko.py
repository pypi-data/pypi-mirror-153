import requests
import pandas as pd
from .utils import validate_dateformat, transfer_date_format, valid_chain
from .configs import COIN_GECHO_CHAIN_DATA

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
    
    def get_chains(self):
        url = f"{self.url}/asset_platforms"
        r = requests.get(url)
        return pd.DataFrame(r.json())

    def get_coin_history(self, coin_id, date):
        if not validate_dateformat(date, "%Y-%m-%d"):
            raise ValueError(f"Invalid date format {date}, should be %Y-%m-%d")
        api_date_format = transfer_date_format(date, "%Y-%m-%d", "%d-%m-%Y")
        url = f"{self.url}/coins/{coin_id}/history"
        params = {
            "date": api_date_format,
            "localization": False,
        }
        r = requests.get(url, params=self.get_params(**params))
        return r.json()

    def get_coin_by_chain_contract(self, chain, contract_addr):
        valid_chain(chain)
        chain_id = COIN_GECHO_CHAIN_DATA[chain]['chain_id']
        url = f"{self.url}/coins/{chain_id}/contract/{contract_addr}"
        r = requests.get(url)
        return r.json()
    
    def get_coin_id_by_chain(self, chain):
        valid_chain(chain)
        return COIN_GECHO_CHAIN_DATA[chain]['coin_id']

    def get_coin_market_inusd_by_chain_contract(self, chain, contract_addr, days_back='max'):
        url = f"{self.url}/coins/{chain}/contract/{contract_addr}/market_chart"
        params = {
            "vs_currency": 'usd',
            "days": days_back,
        }
        r = requests.get(url, params=self.get_params(**params))
        return r.json()
