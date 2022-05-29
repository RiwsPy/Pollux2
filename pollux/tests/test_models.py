from pollux.models.lamps import Lamps
from django.test import TestCase
from django.contrib.gis.geos import Point
from django.db.utils import ProgrammingError
import pytest
from pollux.formats.position import LNG_1M

"""
import pytest
pytestmark = pytest.mark.django_db


def test_truc(lamp):
    Lamps.objects.create(code='1')
    assert True
"""


class ModelsTest(TestCase):
    def setUp(self):
        lamp1_attr = {
            'height': 8.0,
            'position': Point(1, 0),
            'irc': 75,
            'power': 150,
            'colour': 5000,
            'on_motion': False,
            'lowering_night': 10,
            'orientation': 0.0,
            'horizontal_angle': 360.0,
            'nearest_way_dist': -1.0,
            'day_impact': 0.0,
            'night_impact': 0.0
        }
        self.lamp1 = Lamps.objects.create(**lamp1_attr)
        self.lamp1.save()

        lamp2_attr = {
            'height': 8.0,
            'position': Point(2, 0),
            'irc': 75,
            'power': 150,
            'colour': 5000,
            'on_motion': False,
            'lowering_night': 10,
            'orientation': 270.0,
            'horizontal_angle': 180.0,
            'nearest_way_dist': -1.0,
            'day_impact': 0.0,
            'night_impact': 0.0
        }
        self.lamp2 = Lamps.objects.create(**lamp2_attr)
        self.lamp2.save()

        lamp3_attr = {
            'height': 0.0,
            'position': Point(2+LNG_1M, 0),
            'irc': 75,
            'power': 150,
            'colour': 5000,
            'on_motion': False,
            'lowering_night': 10,
            'orientation': 270.0,
            'horizontal_angle': 180.0,
            'nearest_way_dist': -1.0,
            'day_impact': 0.0,
            'night_impact': 0.0
        }
        self.lamp3 = Lamps.objects.create(**lamp3_attr)
        self.lamp3.save()

    def test_create(self):
        self.assertEqual(self.lamp1.way_type, 'road')
        self.assertEqual(self.lamp1.angle_incidence, 70)
        self.assertEqual(self.lamp1.lumens_per_watt, 100)
        self.assertEqual(round(self.lamp1.distance_with_lux(5)), 30)
        self.assertEqual(round(self.lamp1.distance_with_lux(5*4)), 30/2)
        self.assertEqual(round(self.lamp1.height_max_range), 22)
        self.assertEqual(round(self.lamp1.illuminated_height_at(1)), 8)
        self.assertEqual(round(self.lamp1.illuminated_height_at(10)), 4)
        self.assertEqual(self.lamp1.lumens_time(time='day'), 15000)
        self.assertEqual(self.lamp1.lumens_time(time='night'), 13500)
        self.assertFalse(self.lamp1.is_oriented)
        self.assertTrue(self.lamp2.is_oriented)
        self.assertTrue(self.lamp2.is_aligned_with(self.lamp1))

    def test_lux_with_distance(self):
        expected_value = 28.34
        distance = 8.0
        self.assertEqual(round(self.lamp1.lux_with_distance(distance), 2), expected_value)
        self.assertEqual(round(self.lamp1.lux_with_distance(distance*2), 1),
                         round(expected_value/2**2, 1))
