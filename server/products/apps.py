from django.apps import AppConfig
from django.conf import settings


class ProductsConfig(AppConfig):
    # print(settings.DATABASES["default"])
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"
