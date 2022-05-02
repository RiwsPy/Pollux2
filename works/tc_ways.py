from . import Default_works
from api_ext.smmag import Smmag
from formats.position import Position


class Works(Default_works):
    filename = 'tc_ways'
    request_method = Smmag().call
    url = '/api/lines/json?types=ligne&reseaux=SEM'  # TODO: ajouter les trams ?
    query = ""
    COPYRIGHT_ORIGIN = Smmag.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'

    class Model(Default_works.Model):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.name = kwargs['properties']['LIBELLE']
            self.numero = kwargs['properties']['NUMERO']
