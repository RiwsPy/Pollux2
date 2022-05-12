import requests
import os


class BadStatusError(Exception):
    pass


class Api_ext:
    method = 'GET'
    BASE_URL = os.getenv('BASE_URL')

    def call(self, **kwargs) -> dict:
        kwargs['method'] = kwargs.get('method', self.method)
        if 'url' in kwargs:
            kwargs['url'] = self.BASE_URL + str(kwargs['url'])

        try:
            req = requests.request(**kwargs)
        except requests.exceptions.ConnectionError:
            print('Erreur connexion.')
            raise requests.exceptions.ConnectionError

        if req.status_code == 200:
            return req.json()

        print('ERROR status_code', req.status_code)
        if req.status_code == 504 and self.BASE_URL == 'http://overpass-api.de/api/interpreter':
            print('Limite de requête atteinte.')
        raise BadStatusError
