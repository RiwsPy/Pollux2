from . import Osm_works
from django.contrib.gis.geos import LineString
from pollux.models.highways import Highways


class Works(Osm_works):
    filename = 'ways'
    model = Highways
    query = \
        f"""(
            way["highway"="primary"]{Osm_works().BBOX};
            way["highway"="trunk"]{Osm_works().BBOX};
            way["highway"="motorway"]{Osm_works().BBOX};
            way["highway"="secondary"]{Osm_works().BBOX};
            way["highway"="tertiary"]{Osm_works().BBOX};
            way["highway"="primary_link"]{Osm_works().BBOX};
            way["highway"="secondary_link"]{Osm_works().BBOX};
            way["highway"="tertiary_link"]{Osm_works().BBOX};
            way["highway"="motorway_link"]{Osm_works().BBOX};
            way["highway"="trunk_link"]{Osm_works().BBOX};
            way["highway"="residential"]{Osm_works().BBOX};
            way["highway"="service"]{Osm_works().BBOX};
            way["highway"="living_street"]{Osm_works().BBOX};
            way["highway"="unclassified"]{Osm_works().BBOX};
            way["highway"="footway"]["footway"!="sidewalk"]["footway"!="crossing"]{Osm_works().BBOX};
            way["highway"="pedestrian"]{Osm_works().BBOX};
            way["highway"="cycleway"]{Osm_works().BBOX};
            way["highway"="path"]["bicycle"="yes"]{Osm_works().BBOX};
            way["highway"="path"]["bicycle"="designated"]{Osm_works().BBOX};
        );
        (._;>;);
        """

    highway_accepted = (
                'primary', 'trunk', 'motorway', 'secondary', 'tertiary', 'residential', 'service',
                'living_street', 'unclassified', 'footway', 'pedestrian', 'path',
                'primary_link', 'secondary_link', 'tertiary_link', 'cycleway',
                'motorway_link', 'trunk_link')

    def _can_be_output(self, feature, **kwargs) -> bool:
        return super()._can_be_output(feature, **kwargs) and \
               feature['properties'].get('highway') in self.highway_accepted and \
               not feature['properties'].get('footway', False)  # sidewalk, crossing

    def _output_feature_with_model(self, feature: dict) -> dict:
        feature_model = self.Model(**feature).__dict__.copy()
        feature_model['position'] = LineString(feature_model['position'])
        for k, v in feature['properties'].items():
            k_split = k.split(':')
            if len(k_split) < 3:
                continue
            is_parking, is_lane, side = k_split[:3]
            if is_parking != 'parking' or is_lane != 'lane':
                continue
            if v in ('street_side', 'painted_area_only', 'marked',
                     'fire_lane', 'separate', 'on_street', 'half_on_kerb', 'on_kerb') or \
                    v.isdigit(): # parking:lane:both:capacity = 11
                continue
            if v in ('no_parking', 'no_stopping'):
                v = 'no'

            if side in ('right', 'both'):
                feature_model['parking_r'] = v
            if side in ('left', 'both'):
                feature_model['parking_l'] = v

            if feature_model['parking_l'] != 'unknown' and feature_model['parking_r'] == 'unknown':
                ret = 'no' if feature_model['parking_l'] != 'no' else 'yes'
                feature_model['parking_r'] = ret
            elif feature_model['parking_r'] != 'unknown' and feature_model['parking_l'] == 'unknown':
                ret = 'no' if feature_model['parking_r'] != 'no' else 'yes'
                feature_model['parking_l'] = ret
        return feature_model

    def output(self, data: dict, filename: str = '') -> None:
        data = self.convert_to_geojson(data)
        self.model.objects.all().delete()
        for feature in data['features']:
            if not self._can_be_output(feature):
                continue

            if feature['geometry']['type'] == 'MultiLineString':
                # MultiLineString to LineString
                feature['geometry']['coordinates'] = feature['geometry']['coordinates'][0]
            feature = self._output_feature_with_model(feature)
            self.model.objects.create(**feature)

    class Model(Osm_works.Model):
        def __init__(self, **kwargs):
            self.position = kwargs['geometry']['coordinates']
            self.type = kwargs['properties'].get('highway', '')
            self.name = kwargs['properties'].get('name', '')
            self.width = kwargs['properties'].get('width', 0)
            self.lanes = kwargs['properties'].get('lanes', 0)
            self.parking_r = 'unknown'
            self.parking_l = 'unknown'
