# -*- coding: utf-8 -*-
from django.utils.encoding import force_text
from unidecode import unidecode
import re

def strip_spaces(value):
    return re.sub(r'>\s+<', '> <', force_text(value))

def strip_comments(value):
    return re.sub(r'<!--[^>]*-->', '', force_text(value))

def strip_emptylines(value):
    return re.sub(r'\n\s*\n', '\n', force_text(value))

def strip_lines(value):
    return re.sub(r'\r*\n', ' ', force_text(value))

def slugify(value):
    value = unidecode(value)
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)
