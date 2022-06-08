from . import Default_works
from pollux.models.parking_public import Parking_public
from pollux.api_ext.grenoble_alpes_metropole import Gam
from django.contrib.gis.geos import MultiLineString, LineString


class Works(Default_works):
    filename = 'grenoble_parkings'
    model = Parking_public
    request_method = Gam().call
    url = '/opendata/38185-GRE/Stationnement/json/STATIONNEMENT_BARRETTE_VDG_EPSG4326.json'
    query = ""
    COPYRIGHT_ORIGIN = Gam.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'

    def _output_feature_with_model(self, feature: dict) -> dict:
        geo_type = feature['geometry']['type']
        feature = self.Model(**feature).__dict__
        # forcer le MultiLineString
        if geo_type == 'LineString':
            feature['position'] = MultiLineString(LineString(feature['position']))
        else:
            feature['position'] = MultiLineString(LineString(feature['position'][0]))
        return feature

    class Model(Default_works.Model):
        # pas d'équivalent pour perpendicular
        convert_parking_type = {
            None: 'parallel',
            'épis': 'diagonal',
            'long': 'parallel',
            'unknown': 'parallel',
            'mixte': 'mixte',
        }

        convert_fee_type = {
            None: 'unknown',
            'gratuit': 'no',
            'vert': 'yes',
            'orange': 'yes',
            'violet': 'yes',
        }

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.code = kwargs['properties'].get('BARRETTE_ID', 0)
            self.parking_type = self.convert_parking_type[kwargs['properties'].get("BARRETTE_TYPE_NOM")]
            self.fee = self.convert_fee_type[kwargs['properties'].get('BARRETTE_TARIF_NOM')]
            self.way = kwargs['properties'].get('BARRETTE_VOIE_NOMCOMPL', 'unknown') or ''
