from . import Default_cross
from pollux.models.highways import Highways
from pollux.models.parking_public import Parking_public
from django.db.models import Q
from django.contrib.gis.measure import D
from pollux.formats.geojson import Geojson


class Cross(Default_cross):
    def pre_algo(self):
        print('Préparation des routes...')
        self.ways_queryset = Highways.objects.filter(
            (
                ~Q(parking_r='no') & ~Q(parking_r='unknown') |
                ~Q(parking_l='no') & ~Q(parking_l='unknown')
            )
        )
        print(self.ways_queryset.count(), 'routes trouvées.')

        print('Préparation des parkings de voirie...')
        self.parkings_queryset = Parking_public.objects.all()
        print(self.parkings_queryset.count(), 'parkings trouvés.')

    def apply_algo(self):
        super().apply_algo()
        geo = Geojson()
        counter = 0
        counter_max = self.parkings_queryset.count()
        for parking, parking_dict in zip(self.parkings_queryset,
                                         Parking_public.serialize(self.parkings_queryset)['features']):
            counter += 1
            if counter % 100 == 0:
                print(round(counter/counter_max*100, 2), '% effectués.')
            ret = self.ways_queryset.filter(
                position__distance_lte=(parking.position, D(m=5))
            )
            if ret.count() != 1:
                if ret.count() == 0:
                    geo.append(parking_dict)
                continue

        geo.dump('db/parking_lane_not_in_osm.json')
