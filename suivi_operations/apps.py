from django.apps import AppConfig


class SuiviOperationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "suivi_operations"

    def ready(self):
        from . import signals

        return super().ready()
