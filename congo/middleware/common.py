# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.utils.encoding import force_text
import decimal
import logging
import re

class DecimalRoundingMiddleware(object):
    def process_request(self, request):
        decimal_context = decimal.getcontext()
#        decimal_context.rounding = decimal.ROUND_HALF_UP
        decimal_context.rounding = decimal.ROUND_HALF_EVEN
        return None
