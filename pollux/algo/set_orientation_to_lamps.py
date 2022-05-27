from .georepartition_in_array import Repartition_point, adjacent_match
from pollux.works import MAX_BOUND_LNG_LAT
from pollux.works.ways import Works as Highways
from pollux.formats.position import Position
from pollux.models.lamps import Lamps
from . import Default_cross
from django.contrib.gis.geos import Polygon
from collections import defaultdict


class Cross(Default_cross):
    max_range = 12

    def pre_algo(self):
        print('reset')
        lamps_queryset = Lamps.objects.filter(position__within=Polygon.from_bbox(self.bound))
        for lamp in lamps_queryset:
            # Valeurs par défaut
            lamp.orientation = 0.0
            lamp.horizontal_angle = 360.0
            lamp.nearest_way_dist = -1.0
            lamp.save()

        print('Préparation des luminaires...')
        self.ret_lamps = Repartition_point(Lamps.objects.all(),
                                           bound=MAX_BOUND_LNG_LAT,
                                           max_range=self.max_range)

        print('Préparation des voies...')
        self.ret_highways = Repartition_point(Highways.model.objects.all(),
                                              bound=MAX_BOUND_LNG_LAT,
                                              max_range=self.max_range)

    def apply_algo(self):
        self.lamp_to_light_position = dict()
        super().apply_algo()
        for lamp, highway in adjacent_match(self.ret_lamps.array, self.ret_highways.array, max_case_range=1):
            lamp_pos = Position(lamp.position)
            for index, segment in enumerate(zip(highway.position[:-1], highway.position[1:])):
                dist = lamp_pos.distance_cartesian_from_way(*segment)
                current_is_footway = highway.is_footway
                if lamp.max_range(5, 'day') <= dist or dist <= 1 and current_is_footway:
                    # if dist <= 0.2:
                    #    print(f'distance <= 0.2: code {lamp.code}, distance: {dist}', highway.__dict__)
                    continue
                if hasattr(lamp, 'nearest_highway'):
                    nearest_is_footway = lamp.nearest_highway.is_footway
                    if current_is_footway is nearest_is_footway and dist < lamp.nearest_way_dist:
                        # même type mais plus près
                        pass
                    elif not current_is_footway and nearest_is_footway and lamp.way_type == 'road' or\
                            current_is_footway and not nearest_is_footway and lamp.way_type == 'footway':
                        # type différent et type adéquat trouvé
                        pass
                    else:
                        continue

                lamp.nearest_highway = highway
                nearest_position = lamp_pos.nearest_point_from_way(*segment)
                lamp.orientation = round(lamp_pos.orientation(nearest_position), 2)
                lamp.horizontal_angle = 180.0
                lamp.nearest_way_dist = round(dist, 2)
                lamp.save()

                new_feature = TemporaryObject()
                new_feature.position = nearest_position
                new_feature.source = lamp
                new_feature.init_orientation = lamp.orientation
                new_feature.nearest_way_dist = dist
                self.lamp_to_light_position[lamp.pk] = new_feature

    def post_algo(self):
        # recalcule l'orientation des luminaires ayant une position proche (<= 5m)
        # et éclairant dans la même direction (< 30°)
        # TODO: recalculer les différents segments ? Pas forcément pertinent d'éclairer dans la direction inverse

        if len(self.lamp_to_light_position) == 0:
            print('ERROR: self.lamp_to_light_position vide')
            return

        lamp_target_pos = Repartition_point(list(self.lamp_to_light_position.values()),
                                            bound=MAX_BOUND_LNG_LAT,
                                            max_range=5)

        orientation_mod = [0, 180, 90, 270, 45, 135, 225, 315]
        doublon_checked = set()
        nb_doublon_by_lamp = defaultdict(int)
        for feat1, feat2 in adjacent_match(lamp_target_pos.array, lamp_target_pos.array, max_case_range=1):
            doublon_name = feat1.source.code + feat2.source.code
            if feat1.source == feat2.source or doublon_name in doublon_checked or \
                    feat1.source.nearest_highway != feat2.source.nearest_highway or \
                    Position(feat1.position).distance(feat2.position) >= 3 or \
                    feat1.source.height <= 1 or feat2.source.height <= 1:
                continue
            doublon_checked.add(feat2.source.code + feat1.source.code)
            nb_doublon_by_lamp[feat1.source.code] += 1
            nb_doublon_by_lamp[feat2.source.code] += 1

            referenciel = feat1
            other = feat2
            invert_referenciel = False

            if referenciel.source.power < other.source.power:
                # check du plus puissant
                invert_referenciel = True
            elif referenciel.source.power == other.source.power:
                if referenciel.source.height < other.source.height:
                    # check du plus haut
                    invert_referenciel = True
                elif referenciel.source.height == other.source.height:
                    # check du plus près
                    invert_referenciel = referenciel.source.nearest_way_dist > other.source.nearest_way_dist

            if invert_referenciel:
                other, referenciel = referenciel, other

            other.source.orientation = round((other.init_orientation +
                                              orientation_mod[nb_doublon_by_lamp[other.source.code] %
                                                        len(orientation_mod)]
                                              ) % 360,
                                             2)
            other.source.save()

        """
        max_range = 5
        diff_angle_max = 30
        orientation_mod = [0, 180, 90, 270, 45, 135, 225, 315]

        print('Check doublon en cours...')
        lamps_queryset = Lamps.objects.filter(position__within=Polygon.from_bbox(self.bound))
        ret_lamps = Repartition_point(lamps_queryset,
                                      bound=MAX_BOUND_LNG_LAT,
                                      max_range=max_range)
        previous_lamp = None
        nb_doublon = 0
        for lamp, lamp2 in adjacent_match(ret_lamps.array, ret_lamps.array, max_case_range=1):
            if lamp == lamp2 or lamp.orientation == -1 and lamp2.orientation == -1:
                continue
            if previous_lamp != lamp:
                previous_lamp = lamp
                nb_doublon = 0

            distance_between = Position(lamp.position).distance(lamp2.position)
            if distance_between > 5:
                continue

            one_is_circular = (lamp.orientation == -1) ^ (lamp2.orientation == -1)
            have_similar_orientation = True
            if not one_is_circular:
                dif_orientation = abs(lamp.orientation - lamp2.orientation)
                have_similar_orientation = dif_orientation < diff_angle_max or dif_orientation > 360-diff_angle_max

            if have_similar_orientation:
                nb_doublon += 1
                referenciel_lamp = lamp
                other_lamp = lamp2
                invert_referenciel = False

                if not one_is_circular:
                    if referenciel_lamp.power < other_lamp.power:
                        # check du plus puissant
                        invert_referenciel = True
                    elif referenciel_lamp.power == other_lamp.power:
                        if referenciel_lamp.height < other_lamp.height:
                            # check du plus haut
                            invert_referenciel = True
                        elif referenciel_lamp.height == other_lamp.height:
                            if referenciel_lamp.nearest_way_dist > other_lamp.nearest_way_dist:
                                # check du plus près
                                invert_referenciel = True
                elif other_lamp.orientation != -1:
                    invert_referenciel = True

                if invert_referenciel:
                    other_lamp, referenciel_lamp = referenciel_lamp, other_lamp

                other_lamp.orientation = (referenciel_lamp.orientation +
                                          orientation_mod[nb_doublon % len(orientation_mod)]) % 360
                other_lamp.save()
        """


class TemporaryObject:
    pass
