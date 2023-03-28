from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # jetzt weiß die app über signals.py bescheid
    # die App selbst ist ja vorher schon in settings.py, und das ist quasi ne unterdatei der app, die wir hier regsiterieren
    def ready(self):
        import users.signals