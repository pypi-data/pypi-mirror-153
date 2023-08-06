import json

import pytest
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse

from django_data_sdk.collector import DjangoDataTopCollector, DjangoDataBottomCollector


@pytest.fixture()
def default_top_collector():
    request = HttpRequest()
    request.user = AnonymousUser()
    top_collector = DjangoDataTopCollector()
    return top_collector


@pytest.fixture()
def default_bottom_collector():
    request = HttpRequest()
    request.user = AnonymousUser()
    bottom_collector = DjangoDataBottomCollector()
    return bottom_collector


@pytest.fixture(params=["default_top_collector", "default_bottom_collector"])
def all_collector(request):
    yield request.getfixturevalue(request.param)


def test_settings(settings):
    assert settings.DJANGO_DATA_APP_SECRET == "secret"


def test_init(all_collector):
    assert all_collector.request is None
    assert all_collector.response is None
    assert all_collector._request_time is None
    assert all_collector._response_time is None
    assert "context" in all_collector.django_data


def test_django_data(all_collector):
    # be sure django_data is readonly
    with pytest.raises(TypeError):
        all_collector.django_data = {}


def test_attach_request(all_collector):
    request = HttpRequest()
    all_collector.attach_request(request)
    assert all_collector.request is not None
    assert all_collector._request_time is not None
    assert all_collector.response is None
    assert all_collector._response_time is None


def test_attach_response(all_collector):
    response = HttpResponse()
    all_collector.attach_response(response)
    assert all_collector.request is None
    assert all_collector._request_time is None
    assert all_collector.response is not None
    assert all_collector._response_time is not None


def test_do_collect(all_collector):
    assert "context" in all_collector.django_data
    assert "user" not in all_collector.django_data
    assert "meta" not in all_collector.django_data
    assert "request" not in all_collector.django_data
    assert "response" not in all_collector.django_data

    with pytest.raises(RuntimeError):
        all_collector.do_collect()

    request = HttpRequest()
    all_collector.attach_request(request)
    with pytest.raises(RuntimeError):
        all_collector.do_collect()

    response = HttpResponse()
    all_collector.attach_response(response)
    all_collector.do_collect()

    assert "user" in all_collector.django_data
    assert "meta" in all_collector.django_data
    assert "request" in all_collector.django_data
    assert "response" in all_collector.django_data

    # serialization works
    json.dumps(all_collector.django_data)
