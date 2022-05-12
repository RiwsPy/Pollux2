from . import Osm_works


class Works(Osm_works):
    filename = 'buildings'
    model = None
    query = \
        f"""
        (
            nwr[building]{Osm_works().BBOX};
            way[barrier=wall]{Osm_works().BBOX};
            way[barrier=fence]{Osm_works().BBOX};
            node[entrance=yes]{Osm_works().BBOX};
            nwr[access=private]{Osm_works().BBOX};
            nwr[amenity=school]{Osm_works().BBOX};
        );
        (._;>;);
        """

    class Model(Osm_works.Model):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.access = kwargs['properties'].get('access', 'public')
            self.barrier = kwargs['properties'].get('barrier', False)
            self.building = kwargs['properties'].get('building', False)
