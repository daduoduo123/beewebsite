from django.apps import AppConfig


class LoginConfig(AppConfig):
    name = 'login'
    verbose_name = '登录用户拓展'

    def ready(self):
        super(LoginConfig, self).ready()
        from . import signals