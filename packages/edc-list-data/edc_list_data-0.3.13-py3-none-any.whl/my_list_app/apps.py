from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "my_list_app"
    verbose_name = "My List Data"
