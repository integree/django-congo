# -*- coding: utf-8 -*-
from django.utils.formats import number_format as _number_format, get_format
from moneyed.localization import _FORMATTER as FORMATTER, DEFAULT as DEFAULT_FORMAT
from django.utils.translation import to_locale, get_language

def number_format(value, decimal_pos = None, use_l10n = None, force_grouping = False, strip_decimal_part = False):
    number = _number_format(value, decimal_pos, use_l10n, force_grouping)
    if decimal_pos and strip_decimal_part:
        number = number.rstrip('0').rstrip(get_format('DECIMAL_SEPARATOR'))
    return number

def get_money_locale(locale = None):
    if locale is None:
        locale = to_locale(get_language())

    locale_list = FORMATTER.formatting_definitions.keys()
    if locale not in locale_list:
        for l in locale_list:
            if l.split('_')[0].upper() == locale.split('_')[0].upper():
                return l

    return DEFAULT_FORMAT.upper()
