from django.apps import AppConfig


class DrawConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.draw"
    verbose_name = "绘图"

    def ready(self):
        import apps.draw.signals
        import apps.draw.detector
