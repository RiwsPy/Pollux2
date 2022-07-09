from . import Osm_works
from pollux.models.crossings import Crossings
from pollux.formats.geojson import Geojson


class Works(Osm_works):
    filename = "crossings"
    model = Crossings
    query = f"""(
            node["highway"="crossing"]{Osm_works().BBOX};
            way["highway"="footway"]["footway"="crossing"]{Osm_works().BBOX};
        );
        (._;>;);
        """

    def output(self, data: dict, filename: str = "") -> None:
        data = self.convert_data_to_geojson(data)
        geo = Geojson()
        geo.load(data)

        # Set LineString to Point
        for feature in geo["features"]:
            if feature.geometry["type"] == "LineString":
                feature.position = feature.position.force_position()
                feature.geometry["type"] = "Point"

        # geo.dump('db/crossings_output.json')
        super().output(geo)
