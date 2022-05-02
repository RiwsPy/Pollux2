from . import Osm_works


class Works(Osm_works):
    filename = 'shops'
    query = \
        f"""
        (
            node[opening_hours][opening_hours!="24/7"]{Osm_works().BBOX};
        );
        """

    class Model(Osm_works.Model):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.name = kwargs['properties'].get('name', '')
            self.opening_hours = kwargs['properties'].get('opening_hours', '')
