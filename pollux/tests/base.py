from pollux.models.lamps import Lamps
import factory
import pytest

pytestmark = pytest.mark.django_db


class LampsFactory(factory.django.DjangoModelFactory):
    code = '1'

    class Meta:
        model = Lamps
        pass
