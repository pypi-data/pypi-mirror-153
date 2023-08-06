# django-data-history

A Django application that allows you to store detailed data in the change log and display the detailed information in object's history view.

## Install

```
pip install django-data-history
```

## Usage

```

## add app: django_middleware_global_request
## add app: django_static_jquery_ui
## add app: django_data_history
## put django_data_history before django.contrib.admin

INSTALLED_APPS = [
    ...
    "django_middleware_global_request",
    "django_static_jquery_ui",
    'django_data_history',
    ...
    'django.contrib.admin',
    ...
]

## add middleware: django_middleware_global_request.middleware.GlobalRequestMiddleware
## add middleware: django_data_history.middlewares.HttpXRequestIdMiddleware
MIDDLEWARE = [
    ...
    "django_middleware_global_request.middleware.GlobalRequestMiddleware",
    "django_data_history.middlewares.HttpXRequestIdMiddleware",
    ...
]

## add X-Request-Id in nginx config file
## set_proxy_header X-Request-Id $reqid
## Change REQUEST_ID_HEADER to match the request header
REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"

## auto generate request id if the header is not set by nginx
AUTO_GENERATE_REQUEST_ID = True

# default to False, so you must set it to True to enable all models injection.
SAVE_DATA_HISTORIES_FOR_ALL = True 

# if SAVE_DATA_HISTORIES_FOR_ALL==False, then only these models will be injected.
# default to empty.
SAVE_DATA_HISTORIES_FOR = [
    "your_app1.model_name1"
]

# if SAVE_DATA_HISTORIES_FOR_ALL==True, these models will NOT be injected.
# default to:
# [
#    "sessions.session",
#    "contenttypes.contenttype",
#    "admin.logentry",
#    "auth.permission",
# ]
DO_NOT_SAVE_DATA_HISTORIES_FOR = [
    "your_app2.model_name2",
]

```

## Instance's history view

![django-date-history-view-preview](https://github.com/zencore-dobetter/pypi-images/raw/main/django-data-history/django-data-history.png)

## Releases

### v0.1.0

- First release.

### v0.1.1

- Fix ugettext_lazy problem.

### v0.1.2

- Add save_data_histories_for_fk_instance to fix inline edit history missing problem.
