# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import FieldDoesNotExist

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active = True)

class OnSiteManager(models.Manager):
    def __init__(self, site_field_name = None):
        super(OnSiteManager, self).__init__()
        self._site_field_name = site_field_name

    def _get_site_field_name(self):
        if not self._site_field_name:
            try:
                site_field_name = 'site'
                self.model._meta.get_field(site_field_name)
            except FieldDoesNotExist:
                site_field_name = 'sites'
            self._site_field_name = site_field_name
        return self._site_field_name

    def _get_site_field(self):
        if not self._site_field:
            self._site_field = self.model._meta.get_field(self._get_site_field_name())
        return self._site_field

    def _get_kwargs(self):
        site_field = self._get_site_field()
        if isinstance(site_field, models.ManyToManyField):
            lookup = '%s__id__in' % site_field
        else:
            lookup = '%s__id' % site_field
        return {
            lookup: settings.SITE_ID
        }

    def get_queryset(self):
        return super(OnSiteManager, self).get_queryset().filter(**self._get_kwargs())

class CurrentManager(models.Manager):
    def __init__(self, start_date_field_name = 'start_date', end_date_field_name = 'end_date'):
        super(OnSiteManager, self).__init__()
        self._start_date_field_name = start_date_field_name
        self._end_date_field_name = end_date_field_name

    def _get_kwargs(self):
        start_date_lookup = '%s_lte' % self._start_date_field_name
        end_date_lookup = '%s_gte' % self._end_date_field_name
        now = timezone.now()
        return {
            start_date_lookup: now,
            end_date_lookup: now
        }

    def get_queryset(self):
        return super(CurrentManager, self).get_queryset().filter(**self._get_kwargs())

class ActiveOnSiteManager(OnSiteManager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active = True)

class ActiveCurrentManager(CurrentManager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active = True)

class CurrentOnSiteManager(CurrentManager, OnSiteManager):
    def __init__(self, start_date_field_name = 'start_date', end_date_field_name = 'end_date', site_field_name = None):
        CurrentManager.__init__(self, start_date_field_name, end_date_field_name)
        self._site_field_name = site_field_name

    def get_queryset(self):
        kwargs = OnSiteManager._get_kwargs(self)
        return CurrentManager.get_queryset(self).filter(**kwargs)
