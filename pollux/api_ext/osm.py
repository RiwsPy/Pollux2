from . import Api_ext


class Osm(Api_ext):
    BASE_URL = 'http://overpass-api.de/api/interpreter'

    def call(self, query: str, skel_qt: bool = False, **kwargs) -> dict:
        query = get_query(query, out_format="json", end="body", skel_qt=skel_qt)

        return super().call(url="", data=query)


def get_query(query: str,
              out_format: str = "json",
              end: str = "body",
              skel_qt: bool = False) -> bytes:
    ret = f'[out:{out_format}];\n'
    ret += query
    ret += f'\nout {end};'
    if skel_qt:
        ret += '>;out skel qt;'

    return ret.encode('utf-8')
