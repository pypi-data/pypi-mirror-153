
default_app_config = "django_data_history.apps.DjangoDataHistoryConfig"

app_requires = [
    "django_middleware_global_request",
    "django_static_jquery_ui",
]

app_middleware_requires = [
    "django_middleware_global_request.middleware.GlobalRequestMiddleware",
    "django_data_history.middlewares.HttpXRequestIdMiddleware",
]
