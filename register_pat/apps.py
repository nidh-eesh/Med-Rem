from django.apps import AppConfig


class RegisterPatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register_pat'


    def ready(self):
        from notification import updater
        updater.start()