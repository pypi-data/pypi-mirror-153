default_app_config = "django_power_admin.apps.DjangoPowerAdminConfig"

app_requires = [
    "mptt",
    "django_static_fontawesome",
    "django_static_jquery_ui",
    "django_middleware_global_request",
]

app_middleware_requires = [
    "django_middleware_global_request.middleware.GlobalRequestMiddleware",
]
