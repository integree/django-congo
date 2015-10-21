from django.conf import settings as _settings
from appconf import AppConf

settings = _settings

class CongoAppConf(AppConf):
    TEMPLATE_CACHE_BACKEND = None
