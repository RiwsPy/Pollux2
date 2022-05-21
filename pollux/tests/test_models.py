from pollux.models.lamps import Lamps
from django.test import TestCase
from django.contrib.gis.geos import Point
from django.db.utils import ProgrammingError
import pytest

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
            'orientation': -1.0,
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
            'nearest_way_dist': -1.0,
            'day_impact': 0.0,
            'night_impact': 0.0
        }
        self.lamp2 = Lamps.objects.create(**lamp2_attr)
        self.lamp2.save()

    def test_create(self):
        self.assertEqual(self.lamp1.way_type, 'road')
        self.assertEqual(self.lamp1.angle_incidence, 70)
        self.assertEqual(self.lamp1.lumens_per_watt, 100)
        self.assertEqual(round(self.lamp1.distance_with_lux(5)), 30)
        self.assertEqual(round(self.lamp1.distance_with_lux(5*4)), 30/2)
        self.assertEqual(round(self.lamp1.height_max_range), 22)
        self.assertEqual(round(self.lamp1.illuminated_height_at(1)), 8)
        self.assertEqual(round(self.lamp1.illuminated_height_at(10)), 4)
        self.assertEqual(self.lamp1.power_impact(time='day'), 150)
        self.assertEqual(self.lamp1.power_impact(time='night'), 135)
        self.assertFalse(self.lamp1.is_oriented)
        self.assertTrue(self.lamp2.is_oriented)
        self.assertTrue(self.lamp2.is_aligned_with(self.lamp1))
        self.assertEqual(self.lamp2.aligned_power_impact(self.lamp1, time='day'), 300)
        self.assertEqual(self.lamp2.aligned_power_impact(self.lamp1, time='night'), 270)
        self.assertEqual(self.lamp1.aligned_power_impact(self.lamp2, time='day'), 150)
