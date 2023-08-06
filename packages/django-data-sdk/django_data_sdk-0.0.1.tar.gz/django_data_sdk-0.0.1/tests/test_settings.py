import pytest


@pytest.fixture
def change_django_data_sink_settings(settings):
    settings.DJANGO_DATA_SINK_SETTINGS = {
        "partition_prefix": "default_prefix",
        "partition_by": "request_time",  # request_time, response_time in context, and put_time
        "partition_date_format": "%Y-%m-%d",  # default interval day by day
        "app_secret": None,
        "backend": "django_data_sdk.sink.backends.KafkaBackend",
        "backend_kwargs": {},
    }


def test_default_settings():
    from django_data_sdk.conf.settings import DJANGO_DATA_SINK_SETTINGS

    assert (
        DJANGO_DATA_SINK_SETTINGS["backend"]
        == "django_data_sdk.sink.backends.DummyBackend"
    )


def test_change_django_settings(change_django_data_sink_settings, settings):
    from django_data_sdk.conf.settings import DJANGO_DATA_SINK_SETTINGS

    assert (
        DJANGO_DATA_SINK_SETTINGS["backend"]
        == "django_data_sdk.sink.backends.KafkaBackend"
    )
