from . import Osm_works


class Works(Osm_works):
    filename = 'crossings'
    query = \
        f"""
        (
            node[highway=crossing]{Osm_works().BBOX};
            node[highway=steps]{Osm_works().BBOX};
        );
        """
