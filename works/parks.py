from . import Osm_works


class Works(Osm_works):
    filename = 'parks'
    query = \
        f"""
        (
            way[leisure=park]{Osm_works().BBOX};
        );
        """
    skel_qt = True

    class Model(Osm_works.Model):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.name = kwargs['properties'].get('name', '')
