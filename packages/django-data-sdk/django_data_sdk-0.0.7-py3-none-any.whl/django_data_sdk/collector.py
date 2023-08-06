import datetime
import json
import logging
from collections import defaultdict
from typing import Dict, Optional, Any

from django.http import HttpRequest, QueryDict, HttpResponse
from django.utils.datastructures import MultiValueDict

from django_data_sdk.conf.settings import (
    DJANGO_DATA_SCOPE_META,
    DJANGO_DATA_SCOPE_REQUEST,
    DJANGO_DATA_SCOPE_RESPONSE,
    DJANGO_DATA_SCOPE_USER,
    DJANGO_DATA_SINK_SETTINGS,
)
from django_data_sdk.sink.base import Sink


class DjangoDataCollectorBase:
    STEP = None

    def __init__(self):
        self.request: Optional[HttpRequest] = None
        self.response: Optional[HttpResponse] = None

        # django_data is organized into scopes and their related data as a dict
        self._django_data: Dict[str, Dict] = defaultdict(dict)
        self._django_data["context"]["step"] = self.STEP

        self._request_time: Optional[datetime.datetime] = None
        self._response_time: Optional[datetime.datetime] = None

        # sink used for collecting data
        self._sink: Sink = Sink.get_sink_instance(DJANGO_DATA_SINK_SETTINGS)

    @property
    def django_data(self) -> Dict[str, Dict]:
        return self._django_data

    @django_data.setter
    def django_data(self, value):
        raise TypeError("django_data is a readonly attribute")

    def attach_request(self, request: HttpRequest):
        """attach request to this collector"""
        self._request_time = datetime.datetime.now()
        self.request = request

    def attach_response(self, response: HttpResponse):
        """attach response to this collector"""
        self._response_time = datetime.datetime.now()
        self.response = response

    def _check_request_and_response(self):
        if self.request is None:
            raise RuntimeError("request is not attached")
        if self.response is None:
            raise RuntimeError("response is not attached")

    def do_collect(self):
        self._check_request_and_response()
        self._collect_request_data()
        self._collect_response_data()
        try:
            self._sink.put(self.django_data)
        except Exception as e:
            logging.error("sink put error", exc_info=e)

    def _collect_request_data(self):
        self._django_data["context"]["request_time"] = self._request_time.isoformat()
        for k, name in DJANGO_DATA_SCOPE_META.items():
            v = self.request.META.get(k)
            self._django_data["meta"][name] = v

        for k, name in DJANGO_DATA_SCOPE_REQUEST.items():
            v = getattr(self.request, k, None)
            self._django_data["request"][name] = v

        # attach user-related info if any
        if hasattr(self.request, "user"):
            user = self.request.user
        else:
            user = object()
        for k, name in DJANGO_DATA_SCOPE_USER.items():
            v = getattr(user, k, None)
            self._django_data["user"][name] = v

        if "headers" in self._django_data["request"]:
            headers: Dict[str, str] = self._get_request_headers()
            self._django_data["request"]["headers"] = headers

        self._django_data["request"]["body"] = self.parsed_request_body()

    def _collect_response_data(self):
        self._django_data["context"]["response_time"] = self._response_time.isoformat()
        time_cost = self._response_time - self._request_time
        time_cost_microseconds = time_cost.microseconds
        time_cost_milliseconds = time_cost_microseconds / 1000.0
        self._django_data["context"]["time_cost_milliseconds"] = time_cost_milliseconds

        for k, name in DJANGO_DATA_SCOPE_RESPONSE.items():
            v = getattr(self.response, k, None)
            self._django_data["response"][name] = v

        if "headers" in self._django_data["response"]:
            headers: Dict[str, str] = self._get_response_headers()
            self._django_data["response"]["headers"] = headers

        self._django_data["response"]["body"] = self.parsed_response_body()

    def _get_response_headers(self) -> Dict[str, str]:
        if hasattr(self.response, "headers"):
            return {
                self._normalize_header_key(k): v
                for k, v in self.response.headers.items()
            }
        # old version Django
        if hasattr(self.response, "_headers"):
            _header_values = getattr(self.response, "_headers").values()
            return {self._normalize_header_key(k): v for k, v in _header_values}
        return {}

    def _get_request_headers(self) -> Dict[str, str]:
        if hasattr(self.request, "headers"):
            return {
                self._normalize_header_key(k): v
                for k, v in self.request.headers.items()
            }
        return {}

    def request_raw_data(self) -> bytes:
        return self.request.body

    def response_raw_data(self) -> bytes:
        return self.response.content

    def request_form(self) -> QueryDict:
        return self.request.POST

    def request_files(self) -> MultiValueDict:
        return self.request.FILES

    def parsed_request_body(self) -> Optional[Dict[str, Any]]:
        form = self.request_form()
        files = self.request_files()
        if form or files:
            data = dict(form.items())
            for k, v in files.items():
                size = self.size_of_file(v)
                data[k] = {"len": size}
            return data
        return self.request_json()

    def parsed_response_body(self) -> Optional[Dict[str, Any]]:
        return self.response_json()

    def request_json(self):
        try:
            if not self.is_request_json():
                return None
            raw_data = self.request_raw_data()
            if raw_data is None:
                return None

            data = raw_data if isinstance(raw_data, str) else raw_data.decode("utf-8")
            return json.loads(data)
        except ValueError:
            pass

    def response_json(self):
        try:
            if not self.is_response_json():
                return None
            raw_data = self.response_raw_data()
            if raw_data is None:
                return None

            data = raw_data if isinstance(raw_data, str) else raw_data.decode("utf-8")
            return json.loads(data)
        except ValueError:
            pass

    def is_request_json(self) -> bool:
        content_type = self.request.META.get("CONTENT_TYPE")
        return self._is_json_content_type(content_type)

    def is_response_json(self) -> bool:
        # too big to store
        if self.response.streaming:
            return False
        response_headers = self._get_response_headers()
        content_type = response_headers.get("content_type")
        return self._is_json_content_type(content_type)

    @staticmethod
    def size_of_file(file) -> int:
        return file.size

    @staticmethod
    def _is_json_content_type(content_type):
        mt = (content_type or "").split(";", 1)[0]
        return (
            mt == "application/json"
            or (mt.startswith("application/"))
            and mt.endswith("+json")
        )

    @staticmethod
    def _normalize_header_key(k: str) -> str:
        return k.replace("-", "_").lower()


class DjangoDataTopCollector(DjangoDataCollectorBase):
    STEP = "top"

    def __init__(self):
        super(DjangoDataTopCollector, self).__init__()


class DjangoDataBottomCollector(DjangoDataCollectorBase):
    STEP = "bottom"

    def __init__(self):
        super(DjangoDataBottomCollector, self).__init__()
