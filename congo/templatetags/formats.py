# -*- coding: utf-8 -*-
from congo.utils import number_format, get_money_locale
from decimal import Decimal, InvalidOperation
from django import template
from django.utils.numberformat import format
from moneyed import Money, get_currency
from moneyed.localization import format_money, _FORMATTER

register = template.Library()

# decimal

@register.filter
def decimalformat(value):
    value = str(value).rstrip('0') or '0'
    return format(value, '.', 2)

@register.filter
def percentformat(value, decimal_pos = None):
    try:
        value = str(Decimal(value) * 100).rstrip('0') or 0
        return number_format(value, decimal_pos = decimal_pos, strip_decimal_part = True) + u"%"
    except InvalidOperation:
        return value

@register.filter
def ratingformat(value):
    return format(value, '.', 1)

# money

@register.filter
def moneyformat(value, currency = 'PLN', decimal_pos = 2, locale = None):
    locale = get_money_locale(locale)

    if isinstance(value, Money):
        pass
    else:
        value = Money(value, currency = get_currency(str(currency)))

    return format_money(value, decimal_places = decimal_pos, locale = locale)

@register.simple_tag
def money(value, currency = 'PLN', decimal_pos = 2, locale = None):
    return moneyformat(value, currency = currency, decimal_pos = decimal_pos, locale = locale)

# units

@register.filter
def sizeformat(value, convert_unit = True):
    if convert_unit and value > 100:
        value = value / 100
        unit = 'm'
    else:
        unit = 'cm'

    return "%s %s" % (number_format(value, decimal_pos = 2, strip_decimal_part = True), unit)

@register.filter
def capacityformat(value, convert_unit = True):
    if convert_unit and value > 1000:
        value = value / 1000
        unit = 'l'
    else:
        unit = 'ml'

    return "%s %s" % (number_format(value, decimal_pos = 2, strip_decimal_part = True), unit)

@register.filter
def weightformat(value, convert_unit = True):
    if convert_unit and value < 1:
        value = value * 1000
        unit = 'g'
    else:
        unit = 'kg'

    return "%s %s" % (number_format(value, decimal_pos = 2, strip_decimal_part = True), unit)

@register.filter
def voltageformat(value):
    return "%s V" % number_format(value, decimal_pos = 2, strip_decimal_part = True)

@register.filter
def amperageformat(value):
    return "%s A" % number_format(value, decimal_pos = 2, strip_decimal_part = True)

@register.filter
def powerformat(value):
    return "%s W" % number_format(value, decimal_pos = 2, strip_decimal_part = True)
