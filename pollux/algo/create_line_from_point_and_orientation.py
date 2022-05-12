from pollux.formats.position import Position


def create_line(model, range_meter: int = 10) -> dict:
    # Création d'une ligne directionnelle simple
    geo_json = model.serialize(model.objects.all())
    for teammate in geo_json['features']:
        if teammate['properties']['orientation'] != -1:
            p1 = Position(teammate['geometry']['coordinates'])
            p2 = p1.projection(distance=range_meter, orientation=teammate['properties']['orientation'])
            teammate['geometry']['type'] = 'LineString'
            teammate['geometry']['coordinates'] = [p1, p2]
    return geo_json
