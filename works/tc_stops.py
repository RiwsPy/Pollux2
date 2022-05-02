from . import Default_works
from api_ext.smmag import Smmag


class Works(Default_works):
    filename = 'tc_stops'
    request_method = Smmag().call
    url = '/api/points/json?types=stops'
    query = ""
    COPYRIGHT_ORIGIN = Smmag.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'
