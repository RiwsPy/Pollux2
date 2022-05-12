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
            way["highway"="residential"]{Osm_works().BBOX};
            way["highway"="service"]{Osm_works().BBOX};
            way["highway"="living_street"]{Osm_works().BBOX};
            way["highway"="unclassified"]{Osm_works().BBOX};
            way["highway"="footway"]{Osm_works().BBOX};
            way["highway"="pedestrian"]{Osm_works().BBOX};
            way["highway"="path"]["bicycle"="yes"]{Osm_works().BBOX};
            way["highway"="path"]["bicycle"="designated"]{Osm_works().BBOX};
        );
        (._;>;);
        """

    def _can_be_output(self, feature, **kwargs) -> bool:
        return super()._can_be_output(feature, **kwargs) and \
               feature.highway in (
                'primary', 'trunk', 'motorway', 'secondary', 'tertiary', 'residential', 'service',
                'living_street', 'unclassified', 'footway', 'pedestrian', 'path')

    def output(self, data: dict, filename: str = '') -> None:
        data = self.convert_to_geojson(data)
        self.model.objects.all().delete()
        for feature in data['features']:
            if feature['geometry']['type'] == 'MultiLineString':
                # MultiLineString to LineString
                feature['geometry']['coordinates'] = feature['geometry']['coordinates'][0]
            feature = self.Model(**feature).__dict__
            feature['position'] = LineString(feature['position'])
            self.model.objects.create(**feature)

    class Model(Osm_works.Model):
        def __init__(self, **kwargs):
            self.position = kwargs['geometry']['coordinates']
            self.type = kwargs['properties'].get('highway', '')
            self.name = kwargs['properties'].get('name', '')
            self.width = kwargs['properties'].get('width', 0)
            self.lanes = kwargs['properties'].get('lanes', 0)
