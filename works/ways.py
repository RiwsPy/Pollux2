from . import Osm_works
from formats.geojson import Geo_Feature


class Works(Osm_works):
    filename = 'ways'
    query = \
        f"""
        (
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

    def _can_be_output(self, feature: Geo_Feature, **kwargs) -> bool:
        return super()._can_be_output(feature, **kwargs) and feature.highway in (
            'primary', 'trunk', 'motorway', 'secondary', 'tertiary', 'residential', 'service',
            'living_street', 'unclassified', 'footway', 'pedestrian', 'path')

    class Model(Osm_works.Model):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.highway = kwargs['properties'].get('highway', '')
            self.name = kwargs['properties'].get('name', '')
            self.width = kwargs['properties'].get('width', 0)
            self.lanes = kwargs['properties'].get('lanes', 0)
