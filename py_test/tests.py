from django.contrib.auth.models import User
from httpx import Client
import pytest

from django.core.exceptions import ObjectDoesNotExist
from simple_db.models import Thing


@pytest.mark.django_db
def test_get_thing():
    # Раскомментировать, чтобы вызвать ошибку
    # thing = Thing.objects.create(name='One_Thing', amount=3)
    with pytest.raises(ObjectDoesNotExist):
        thing = Thing.objects.get(name='One_Thing')


urls = ['http://server1:8000/json', 'http://server2:8000/json']
@pytest.mark.parametrize('url', urls)
def test_api(url):
    with Client() as client:
        print(url)
        response = client.get(url)
    assert response.status_code == 200
    assert type(response.json()) == dict
