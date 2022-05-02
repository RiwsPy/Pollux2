from . import Osm_works


class Works(Osm_works):
    filename = 'vending_machine'
    query = \
        f"""
        (
            node[vending=condoms]{Osm_works().BBOX};
        );
        """