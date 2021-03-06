from congo.conf import settings
from congo.maintenance.filters import LogLevelFilter, AuditLevelFilter, SiteLanguage
from congo.templatetags.common import or_blank
from congo.utils.classes import get_class
from django.contrib import messages
from django.db import models
from django.utils.translation import ugettext_lazy as _

modeladmin_name = settings.CONGO_ADMIN_MODEL
modeladmin = get_class(modeladmin_name)

class SiteAdmin(modeladmin):
    list_display = ('domain', 'language', 'is_active')
    list_filter = (SiteLanguage, 'is_active',)
    search_fields = ('domain',)

class ConfigAdmin(modeladmin):
    list_display = ('name', 'value', 'use_cache', 'load_at_startup')
    list_filter = ('use_cache', 'load_at_startup',)
    search_fields = ('name', 'description',)

class LogAdmin(modeladmin):
    list_display = ('name', 'colored_level', 'message', 'user', 'date')
    list_filter = ('name', LogLevelFilter, 'user',)
    fields = ('name', 'level', 'message', 'user', 'date', 'render_args')
    readonly_fields = ('user', 'date', 'render_args')
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

    def render_args(self, obj):
        return or_blank(obj.args)
    render_args.short_description = _("Extra details")
    render_args.admin_order_field = 'args'

class AuditAdmin(modeladmin):
    list_display = ('render_name', 'level', 'frequency', 'result', 'is_active')
    list_filter = (AuditLevelFilter, 'frequency', 'result', 'is_active',)
    readonly_fields = ('render_description', 'result', 'render_details')
    search_fields = ('test', 'details')
    filter_horizontal = ('auditors',)
    actions = ('run_test',)

    fieldsets = (
        (None, {
            'fields': ('test', 'render_description', 'level', 'frequency', 'is_active', 'auditors',)
        }),
        (_("Results"), {
            'fields': ('result', 'render_details')
        }),
    )

    def render_name(self, obj):
        return or_blank(obj.name)
    render_name.short_description = _("Name")
    render_name.admin_order_field = 'test'

    def render_description(self, obj):
        test = obj._get_test()
        if test:
            return or_blank(test.description)
        return or_blank(None)
    render_description.short_description = _("Description")

    def render_details(self, obj):
        return or_blank(obj.details)
    render_details.short_description = _("Extra details")
    render_details.admin_order_field = 'details'
    render_details.allow_tags = True

    # actions
    def run_test(self, request, queryset):
        i = j = 0
        for audit in queryset:
            if audit.run_test(request.user):
                i += 1
            j += 1
        message = _("Audit tests invoked")
        level = messages.INFO if i == j else messages.ERROR
        self.message_user(request, "%s (%s / %s)" % (message, i, j), level = level)
    run_test.short_description = u"Run audit test"

class CronAdmin(modeladmin):
#    list_display = ('render_name', 'frequency', 'is_active', 'run_now_anchor')
    list_display = ('render_name', 'frequency', 'is_active')
    list_filter = ('frequency', 'is_active',)
    fields = ('job', 'render_description', 'frequency', 'is_active')
    readonly_fields = ('render_description',)
    search_fields = ('task',)
    actions = ('run_job',)

    def render_name(self, obj):
        return obj.name
    render_name.short_description = _("Name")
    render_name.admin_order_field = 'job'

    def render_description(self, obj):
        job = obj._get_job()
        if job:
            return or_blank(job.description)
        return or_blank(None)
    render_description.short_description = _("Description")

#    def run_now_anchor(self, obj):
#        return u"<a href='%s'>%s</a>" % (obj.get_absolute_url(), _("Run now"))
#    run_now_anchor.short_description = _("Run now")
#    run_now_anchor.allow_tags = True

    # actions
    def run_job(self, request, queryset):
        i = j = 0
        for cron in queryset:
            if cron.run_job(request.user):
                i += 1
            j += 1
        message = _("CRON jobs invoked")
        level = messages.INFO if i == j else messages.ERROR
        self.message_user(request, "%s (%s / %s)" % (message, i, j), level = level)
    run_job.short_description = u"Run CRON job"

class UrlRedirectAdmin(modeladmin):
    list_display = ('old_url', 'redirect_url', 'rewrite_tail', 'is_permanent_redirect')
    list_filter = ('rewrite_tail', 'is_permanent_redirect',)
    search_fields = ('old_url', 'redirect_url',)
