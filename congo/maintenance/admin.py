from congo.conf import settings
from congo.maintenance.filters import LogLevelFilter
from congo.utils.classes import get_class
from django.db import models
from django.utils.translation import ugettext_lazy as _

modeladmin_name = settings.CONGO_ADMIN_MODEL
modeladmin = get_class(modeladmin_name)

class SiteAdmin(modeladmin):
    list_display = ('domain', 'language', 'is_active')
    list_filter = ('language', 'is_active',)
    search_fields = ('domain',)

class ConfigAdmin(modeladmin):
    list_display = ('name', 'value', 'use_cache', 'load_at_startup')
    list_filter = ('use_cache', 'load_at_startup',)
    search_fields = ('name', 'description',)

class LogAdmin(modeladmin):
    list_display = ('name', 'colored_level', 'message', 'user', 'date')
    list_filter = ('name', LogLevelFilter, 'user',)
    search_fields = ('name', 'message', 'args')
    date_hierarchy = 'date'

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(LogAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if type(db_field) == models.TextField:
            field.widget.attrs['rows'] = 20
        return field

    def colored_level(self, obj):
        return obj.render_level(obj.level)
    colored_level.short_description = _("Level")
    colored_level.allow_tags = True
    colored_level.admin_order_field = 'level'

class CronAdmin(modeladmin):
    list_display = ('render_name', 'frequency', 'is_active', 'run_now_anchor')
    list_filter = ('frequency', 'is_active',)
    search_fields = ('task',)

    def render_name(self, obj):
        return obj.name
    render_name.short_description = _("Name")
    render_name.admin_order_field = 'job'

    def run_now_anchor(self, obj):
        return u"<a href='%s'>%s</a>" % (obj.get_absolute_url(), _("Run now"))
    run_now_anchor.short_description = _("Run now")
    run_now_anchor.allow_tags = True

class UrlRedirectAdmin(modeladmin):
    list_display = ('old_url', 'redirect_url', 'rewrite_tail', 'is_permanent_redirect')
    list_filter = ('rewrite_tail', 'is_permanent_redirect',)
    search_fields = ('old_url', 'redirect_url',)
