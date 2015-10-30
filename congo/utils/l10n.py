# -*- coding: utf-8 -*-
from moneyed.localization import _FORMATTER as FORMATTER, DEFAULT as DEFAULT_FORMAT
from django.utils.translation import to_locale, get_language

def get_money_locale(locale = None):
    if locale is None:
        locale = to_locale(get_language())

    locale_list = FORMATTER.formatting_definitions.keys()
    if locale not in locale_list:
        for l in locale_list:
            if l.split('_')[0].upper() == locale.split('_')[0].upper():
                return l

    return DEFAULT_FORMAT.upper()
