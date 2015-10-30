# -*- coding: utf-8 -*-
from congo.conf import settings
import decimal

class CommonMiddleware(object):
    def process_request(self, request):
        admin_path = settings.CONGO_ADMIN_PATH
        if request.path.startswith(admin_path):
            request.is_admin_backend = True
        else:
            request.is_admin_backend = False

class DecimalRoundingMiddleware(object):
    def process_request(self, request):
        decimal_context = decimal.getcontext()
#        decimal_context.rounding = decimal.ROUND_HALF_UP
        decimal_context.rounding = decimal.ROUND_HALF_EVEN
        return None
