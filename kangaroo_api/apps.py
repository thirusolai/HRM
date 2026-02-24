from django.apps import AppConfig


class KangarooApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kangaroo_api"

    def ready(self):
        """
        Initialize API documentation when the app is ready
        """
        # Import and register API documentation components
        import kangaroo_api.schema  # noqa
