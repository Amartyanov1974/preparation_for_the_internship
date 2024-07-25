from django.contrib.auth.models import User
import pytest

from django.core.exceptions import ObjectDoesNotExist
from simple_db.models import Thing


@pytest.mark.django_db
def test_get_thing():
    # Раскомментировать, чтобы вызвать ошибку
    # thing = Thing.objects.create(name='One_Thing', amount=3)
    with pytest.raises(ObjectDoesNotExist):
        thing = Thing.objects.get(name='One_Thing')


@pytest.mark.parametrize('numer, result', [(1, 1), (2, 4), (3, 9)])
def test_quad(numer, result):
    assert numer*numer == result
