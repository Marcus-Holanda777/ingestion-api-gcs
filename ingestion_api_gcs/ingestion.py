import requests
from datetime import datetime


class ApiCurrencyError(Exception):
    ...

class ApiCurrencyRequests:
    def __init__(self, token: str, endpoint: str) -> None:
        self.token = token
        self.endpoint = endpoint
        self.headers = self.headers()
    
    def headers(self):
        return {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/129.0.0.0 Safari/537.36'
            ),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'apikey': self.token
        }

    def requests(self, start: str, **kwargs):
        kwargs['headers'] = self.headers
        
        try:
            response =  requests.get(
                self.endpoint + f'/{start}', 
                **kwargs
            )

            cod_status = response.status_code
            if cod_status != 200:
                error = response.json().values()
                raise ApiCurrencyError(*error)
            
        except requests.exceptions.RequestException:
            raise
        else:
            return response.json()

class Ingestion(ApiCurrencyRequests):
    def __init__(
        self, 
        token: str, 
        endpoint: str = 'https://api.freecurrencyapi.com/v1'
    ) -> None:
        
        super().__init__(token, endpoint)
    
    @property
    def status(self):
        return self.requests('/status')
    
    def lista_moedas(
        self, 
        currencies: list[str] = []
    ):
        
        kwargs = dict()
        kwargs |= {'params': {'currencies': self.list_join(currencies)}}

        return self.requests('/currencies', **kwargs)
    
    def taxa_cambio(
        self, 
        base_currency: str = None, 
        currencies: list[str] = []
    ):
        kwargs = dict()
        kwargs |= {
            'params': {
                'base_currency': base_currency, 
                'currencies': self.list_join(currencies)
            }
        }

        return self.requests('/currencies', **kwargs)
    
    def historico(
        self, 
        date: datetime, 
        base_currency=None, 
        currencies=[]
    ):
        kwargs = dict()
        kwargs |= {
            'params': {
                'date': f'{date:%Y-%m-%d}',
                'base_currency': base_currency,
                'currencies': self.list_join(currencies)
            }
        }
        
        return self.requests('/historical', **kwargs)
    
    def list_join(self, seq: list[str]):
        return ','.join(seq)