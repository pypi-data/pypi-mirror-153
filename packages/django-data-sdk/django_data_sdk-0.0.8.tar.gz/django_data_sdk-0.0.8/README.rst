How to use django_data_sdk in your django project
=========================================================

settings.INSTALLED_APPS
--------------------------------------------

.. code-block:: python

    INSTALLED_APPS = [
        # other apps ...
        "django_data_sdk",
        # other apps ...
    ]

Install middleware to settings.MIDDLEWARE
--------------------------------------------

.. code-block:: python

    MIDDLEWARE = [
        "django_data_sdk.middleware.DjangoDataTopMiddleware",
        # other middlewares
        "django_data_sdk.middleware.DjangoDataBottomMiddleware",
    ]


Configure DJANGO_DATA related settings
------------------------------------------

.. code-block:: python

    DJANGO_DATA_SINK_SETTINGS = {
        "partition_prefix": "default_prefix",
        "partition_by": "request_time",  # request_time, response_time in context, and put_time
        "partition_date_format": "%Y-%m-%d",  # default interval day by day
        "app_secret": None,
        "backend": "django_data_sdk.sink.backends.DummyBackend", # DummyBackend or KafkaBackend
        "backend_kwargs": {},
        "sink_mode": mode.DIRECT,  # DIRECT or CELERY
    }


Restart the service and check your data from the sink backend
------------------------------------------------------------------

