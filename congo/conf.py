from django.conf import settings
from appconf import AppConf

class CongoAppConf(AppConf):
    CUSTOM_VAR = "This is custom VAR"
