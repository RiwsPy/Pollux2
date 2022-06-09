from . import Osm_works
from django.contrib.gis.geos import LineString, MultiLineString
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
            way["highway"="service"]["access"!="private"]{Osm_works().BBOX};
            way["highway"="living_street"]{Osm_works().BBOX};
            way["highway"="unclassified"]["access"!="private"]{Osm_works().BBOX};
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
               not feature['properties'].get('footway', False) and \
               feature['properties'].get('access') != "private"

    def _output_feature_with_model(self, feature: dict) -> dict:
        feat_geo_type = feature['geometry']['type']
        feature_model = self.Model(**feature).__dict__.copy()
        if feat_geo_type == 'LineString':
            feature_model['position'] = MultiLineString(LineString(feature_model['position']))
        else:
            feature_model['position'] = MultiLineString(LineString(feature_model['position'][0]))
        for k, v in feature['properties'].items():
            k_split = k.split(':')
            if len(k_split) < 3:
                continue
            is_parking, is_lane, side = k_split[:3]
            if is_parking != 'parking' or is_lane != 'lane':
                continue
            if v in ('street_side', 'painted_area_only', 'fire_lane',
                     'separate', 'on_street', 'half_on_kerb', 'on_kerb') or \
                    v.isdigit():  # parking:lane:both:capacity = 11
                continue
            elif v in ('no_parking', 'no_stopping'):
                v = 'no'
            elif v == 'marked':
                v = 'yes'

            if side in ('right', 'both'):
                feature_model['parking_r'] = v
            if side in ('left', 'both'):
                feature_model['parking_l'] = v

        return feature_model

    class Model(Osm_works.Model):
        def __init__(self, **kwargs):
            self.position = kwargs['geometry']['coordinates']
            self.highway = kwargs['properties'].get('highway', '')
            self.name = kwargs['properties'].get('name', '')[:100]
            self.width = kwargs['properties'].get('width', 0)
            self.lanes = kwargs['properties'].get('lanes', 0)
            self.maxspeed = kwargs['properties'].get('maxspeed', 0)
            self.oneway = kwargs['properties'].get('oneway', 'no')
            self.parking_r = 'unknown'
            self.parking_l = 'unknown'
