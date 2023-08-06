import os
from typing import Any

from django.conf import settings as django_settings
from django.core.signals import setting_changed

from ..sink import mode

DJANGO_DATA_SCOPE_META_DEFAULT = {
    "REQUEST_METHOD": "request_method",
    "QUERY_STRING": "query_string",
    "PATH_INFO": "path_info",
    "wsgi.multithread": "wsgi_multithread",
    "wsgi.multiprocess": "wsgi_multiprocess",
    "REMOTE_ADDR": "remote_addr",
    "REMOTE_HOST": "remote_host",
    "REMOTE_PORT": "remote_port",
    "SERVER_NAME": "server_name",
    "SERVER_PORT": "server_port",
    "HTTP_HOST": "http_host",
    "HTTP_CONNECTION": "http_connection",
    "HTTP_UPGRADE_INSECURE_REQUESTS": "http_upgrade_insecure_requests",
    "HTTP_USER_AGENT": "http_user_agent",
    "HTTP_ACCEPT": "http_accept",
    "HTTP_ACCEPT_ENCODING": "http_accept_encoding",
    "HTTP_ACCEPT_LANGUAGE": "http_accept_language",
    "HTTP_CACHE_CONTROL": "http_cache_control",
    "CONTENT_LENGTH": "content_length",
    "CONTENT_TYPE": "content_type",
}

DJANGO_DATA_SCOPE_REQUEST_DEFAULT = {
    "GET": "get",
    "POST": "post",
    "COOKIES": "cookies",
    "content_type": "content_type",
    "FILES": "files",
    "request_id": "request_id",
    "headers": "headers",
}

DJANGO_DATA_SCOPE_USER_DEFAULT = {
    "id": "user_id",
    "email": "email",
}

DJANGO_DATA_SCOPE_RESPONSE_DEFAULT = {
    "status_code": "status_code",
    "reason_phrase": "reason_phrase",
    "charset": "charset",
    "streaming": "streaming",
    "closed": "closed",
    "headers": "headers",
}

DJANGO_DATA_SCOPE_META = (
    getattr(django_settings, "DJANGO_DATA_SCOPE_META", None)
    or DJANGO_DATA_SCOPE_META_DEFAULT
)
DJANGO_DATA_SCOPE_REQUEST = (
    getattr(django_settings, "DJANGO_DATA_SCOPE_REQUEST", None)
    or DJANGO_DATA_SCOPE_REQUEST_DEFAULT
)

DJANGO_DATA_SCOPE_USER = (
    getattr(django_settings, "DJANGO_DATA_SCOPE_USER", None)
    or DJANGO_DATA_SCOPE_USER_DEFAULT
)

DJANGO_DATA_SCOPE_RESPONSE = (
    getattr(django_settings, "DJANGO_DATA_SCOPE_RESPONSE", None)
    or DJANGO_DATA_SCOPE_RESPONSE_DEFAULT
)

DJANGO_DATA_SINK_THREAD_POOL_SIZE = os.cpu_count()

DJANGO_DATA_SINK_SETTINGS = getattr(django_settings, "DJANGO_DATA_SINK_SETTINGS", None)
if DJANGO_DATA_SINK_SETTINGS is None:
    DJANGO_DATA_SINK_SETTINGS = {
        "partition_prefix": "default_prefix",
        "partition_by": "request_time",  # request_time, response_time in context, and put_time
        "partition_date_format": "%Y-%m-%d",  # default interval day by day
        "app_secret": None,
        "backend": "django_data_sdk.sink.backends.DummyBackend",
        "backend_kwargs": {},
        "sink_mode": mode.DIRECT,
    }


# for testing purpose
def reload_settings(*args: Any, **kwargs: Any) -> None:
    setting, value = kwargs["setting"], kwargs["value"]
    globals()[setting] = value


setting_changed.connect(reload_settings)
