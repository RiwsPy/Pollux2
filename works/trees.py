from . import Default_works
from api_ext.grenoble_alpes_metropole import Gam
import datetime


class Works(Default_works):
    filename = 'trees'
    request_method = Gam().call
    url = '/opendata/38185-GRE/EspacePublic/json/ARBRES_TERRITOIRE_VDG_EPSG4326.json'
    query = ""
    COPYRIGHT_ORIGIN = Gam.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'

    class Model(Default_works.Model):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            properties = kwargs['properties']
            self.id = properties['ELEM_POINT_ID']
            self.code = properties['NOM']
            self.taxon = (properties['GENRE_BOTA'] or '') + ' ' + (properties['ESPECE'] or '')
            self.planted_date = int(properties['ANNEEDEPLANTATION'] or 0)
            if self.planted_date:
                age = datetime.date.today().year - self.planted_date
                height = round(max(3, min(int(age/2), 15)))
            else:
                height = 7
            self.height = height
