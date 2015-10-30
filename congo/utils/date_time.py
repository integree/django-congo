# -*- coding: utf-8 -*-
from django.utils import timezone

def years_ago(years, from_date = None):
    if from_date is None:
        from_date = timezone.now()
    try:
        return from_date.replace(year = from_date.year - years)
    except:
        return from_date.replace(month = 2, day = 28, year = from_date.year - years)
