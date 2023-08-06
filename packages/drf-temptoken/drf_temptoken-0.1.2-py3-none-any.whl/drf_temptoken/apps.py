from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drf_temptoken'

    def ready(self, *args, **kwargs):
        from drf_temptoken import signals
