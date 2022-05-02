from . import Works_cross
from works import lamps, ways
from formats.position import Position
from collections import defaultdict
import numpy as np
import json
import os
from works import BASE_DIR
import math


class Cross(Works_cross):
    max_range = 12
    filename = __file__

    def load(self, *teams, **kwargs) -> None:
        teams = teams or ([lamps], [ways])
        super().load(*teams, **kwargs, segment=True)

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        id = 0
        dict_values = dict()
        old_blue_teammate = None
        lamp_is_high = True
        correspondances_lamp_way = defaultdict(list)
        for blue_teammate, red_teammate, distance in self._iter_double_and_range():
            correspondances_lamp_way[blue_teammate.id].append(red_teammate)
            if old_blue_teammate != blue_teammate:
                old_blue_teammate = blue_teammate
                id += 1
                lamp_is_high = blue_teammate.height > 5 and not blue_teammate.on_motion
            if not lamp_is_high and distance > self.max_range/2:
                continue

            has_segment = blue_teammate['properties'].get('_nearest_segment')
            if has_segment:
                current_is_footway = self.is_footway(red_teammate.__dict__)
                nearest_is_footway = self.is_footway(blue_teammate['properties']['_nearest_segment'])
                current_is_nearest = distance < blue_teammate['properties']['_nearest_distance']
                # element de même type : priorité à l'élément le plus proche
                if current_is_nearest and current_is_footway is nearest_is_footway:
                    # print('plus près et type équivalent')
                    # print(blue_teammate['properties'].get('_nearest_segment'), '<< ', red_teammate.__dict__)
                    pass
                elif distance < self.max_range/2 and not current_is_footway and not nearest_is_footway:
                    # print(f'distance < {self.max_range/2} et type route')
                    # print(blue_teammate['properties'].get('_nearest_segment'), '<< ', red_teammate.__dict__)
                    pass
                # élément de type différent
                # si le luminaire est bas (<= 5m), la priorité est donnée aux chemins
                # sinon, la priorité est donnée aux routes
                elif not lamp_is_high and (current_is_footway and not nearest_is_footway) or\
                        lamp_is_high and not current_is_footway and nearest_is_footway:
                    # print('feu pas adapté')
                    # print(blue_teammate['properties'].get('_nearest_segment'), '<< ', red_teammate.__dict__)
                    pass
                else:
                    continue

            blue_teammate['properties']['_nearest_segment'] = red_teammate.__dict__
            blue_teammate['properties']['_nearest_distance'] = distance

            h_position = blue_teammate.position.nearest_point_from_way(*red_teammate.positions)
            orientation = blue_teammate.position.orientation(h_position)
            blue_teammate['properties'][self.value_attr]['orientation'] = round(float(orientation), 2)

            dict_values[id] = blue_teammate

        self.check_doublon()

        for lamp_value in dict_values.values():
            del lamp_value['properties']['_nearest_distance']
            del lamp_value['properties']['_nearest_segment']

        self.create_form('polygon', 20)

    orientation_mod = {0: 0, 1: 180, 2: 90, 3: 270}

    def check_doublon(self):
        # recalcule l'orientation des luminaires ayant une position proche (<= 5m)
        # et éclairant dans la même direction (< 30°)
        # TODO: recalculer les différents segments ? Pas forcément pertinent d'éclairer dans la direction inverse
        dim = self.bound_to_array(self.bound, side=3)
        np_array = np.empty(dim, dtype=np.dtype('O'))
        np_array = self.repartition_in_array(self.teams[0]["features"], np_array, max_range=3)
        for referentiel in self.teams[0].features:
            if not referentiel['properties'].get('_nearest_segment'):
                continue
            referentiel_position = referentiel.position
            referentiel_case = self.feature_position_case(referentiel, bound=self.bound, max_range=3)
            for i in range(referentiel_case[0] - 1, referentiel_case[0] + 2):
                for j in range(referentiel_case[1] - 1, referentiel_case[1] + 2):
                    try:
                        lamp_features = np_array[(i, j)] or ()
                    except IndexError:
                        continue

                    nb_doublon = 0
                    orientation_base = referentiel._pollux_values['orientation']
                    for lamp in lamp_features:
                        if lamp == referentiel or \
                                not lamp['properties'].get('_nearest_segment'):
                            continue

                        geo_distance_between = referentiel_position.distance(lamp.position)
                        dif_orientation = abs(orientation_base - lamp._pollux_values['orientation'])
                        have_similar_orientation = dif_orientation < 30 or dif_orientation > 330
                                                   # or referentiel._pollux_values['orientation'] is None and \
                                                   # lamp._pollux_values['orientation'] is None
                        if geo_distance_between <= 5 and have_similar_orientation:
                            nb_doublon += 1
                            farest_lamp = referentiel
                            if lamp['properties']['_nearest_distance'] > referentiel['properties']['_nearest_distance']:
                                farest_lamp = lamp
                            orientation_mod = self.orientation_mod.get(nb_doublon%4)

                            farest_lamp['properties']['_pollux_values']['orientation'] = (
                                farest_lamp['properties']['_pollux_values']['orientation'] + orientation_mod) % 360

    def create_form(self, form_type, range_meter: int) -> None:
        if form_type == 'line':
            self.create_line(range_meter)
        elif form_type == 'polygon':
            self.create_polygon()
        elif form_type == 'basic':
            self.export_basic_data()

    def create_line(self, range_meter: int) -> None:
        # Création d'une ligne directionnelle simple
        for teammate in self.teams[0].features:
            teammate_orientation = teammate.properties[self.value_attr].get('orientation')
            if teammate_orientation:
                teammate['geometry']['type'] = 'MultiLineString'
                p1 = teammate.position
                p2 = teammate.position.projection(distance=range_meter, orientation=teammate_orientation)
                teammate['geometry']['coordinates'] = [[p1, p2]]

    def create_polygon(self) -> None:
        # Création d'un rectangle symbolant la zone éclairée approximative
        for teammate in self.teams[0].features:
            teammate_orientation = teammate.properties[self.value_attr].get('orientation')
            lamp_height = teammate.properties['height']
            max_range = lamp_height / math.tan(math.radians(20))
            if lamp_height > 1 and teammate_orientation is not None:  # flux orienté
                position1 = teammate.position.projection(distance=max_range, orientation=teammate_orientation + 90)
                position2 = teammate.position.projection(distance=max_range, orientation=teammate_orientation + 270)
                position3 = position2.projection(distance=max_range*4/5, orientation=teammate_orientation)
                position4 = position3.projection(distance=max_range*2, orientation=teammate_orientation + 90)
                positions = [
                    position1,
                    position2,
                    position3,
                    position4,
                ]
            else:  # flux circulaire
                if max_range <= 1:
                    max_range = 12
                positions = [
                    teammate.position.projection(distance=max_range/2, orientation=i * 90)
                    for i in range(4)
                ]

            teammate['geometry']['type'] = 'Polygon'
            teammate['geometry']['coordinates'] = Position([positions])

    def export_basic_data(self) -> None:
        w = lamps.Works()
        with open(os.path.join(BASE_DIR, 'db', w.filename+'_with_orientation.json'), 'w+') as file:
            print('Ecriture de', w.filename+'_with_orientation.json')
            json.dump(self.teams[0], file)

    @staticmethod
    def is_footway(feature) -> bool:
        return feature['properties']['highway'] in ('footway', 'pedestrian', 'path') or \
               not feature['properties'].get('name')
