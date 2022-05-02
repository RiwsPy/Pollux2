from . import Osm_works


class Works(Osm_works):
    filename = 'churchs'
    skel_qt = True
    query = \
        f"""
        (
          nwr[building=church]{Osm_works().BBOX};
          nwr[amenity=place_of_worship]{Osm_works().BBOX};
        );
        """

    class Model(Osm_works.Model):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.name = kwargs['properties'].get('name', '')
