from django.apps import AppConfig


class QuizhubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quizhub'

    def ready(self):
        import quizhub.signals
