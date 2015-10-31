# -*- coding: utf-8 -*-
from admin_tools.menu import items, Menu
from admin_tools.menu.items import AppList, MenuItem
from congo.conf import settings
from django.apps import apps as django_apps
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _

class OrderedAppList(AppList):
    def init_with_context(self, context):
        """
        Please refer to the :meth:`~admin_tools.menu.items.MenuItem.init_with_context`
        documentation from :class:`~admin_tools.menu.items.MenuItem` class.
        """
        items = self._visible_models(context['request'])
        apps = {}
        for model, perms in items:
            if not perms['change']:
                continue

            app_label = model._meta.app_label
            if app_label not in apps:
                apps[app_label] = {
                    'title': django_apps.get_app_config(app_label).verbose_name,
                    'url': self._get_admin_app_list_url(model, context),
                    'models_dict': {}
                }

            apps[app_label]['models_dict'][model._meta.object_name] = {
                'title': model._meta.verbose_name_plural,
                'url': self._get_admin_change_url(model, context)
            }

        app_order_dict = SortedDict(settings.ADMIN_TOOLS_APP_ORDER)
        added_app_list = []
        added_model_list = []

        for app_label in app_order_dict.keys():
            if app_label in apps:
                item = MenuItem(title = apps[app_label]['title'], url = apps[app_label]['url'])
                added_app_list.append(app_label)

                for model_name in app_order_dict[app_label]:
                    if model_name in apps[app_label]['models_dict']:
                        model_dict = apps[app_label]['models_dict'][model_name]
                        model_path = '%s.%s' % (app_label, model_name)
                        added_model_list.append(model_path)
                        item.children.append(MenuItem(**model_dict))

                for model_name in sorted(apps[app_label]['models_dict'].keys()):
                    model_dict = apps[app_label]['models_dict'][model_name]
                    model_path = '%s.%s' % (app_label, model_name)
                    if not model_path in added_model_list:
                        item.children.append(MenuItem(**model_dict))

                self.children.append(item)

        for app in sorted(apps.keys()):
            if app not in added_app_list:
                app_dict = apps[app]
                item = MenuItem(title = app_dict['title'], url = app_dict['url'])

                for model_name in sorted(apps[app]['models_dict'].keys()):
                    model_dict = apps[app]['models_dict'][model_name]
                    model_path = '%s.%s' % (app, model_name)
                    if not model_path in added_model_list:
                        item.children.append(MenuItem(**model_dict))

                self.children.append(item)

class OrderedMenu(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        super(OrderedMenu, self).init_with_context(context)

        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            OrderedAppList(
                _('Applications'),
                exclude = ('django.contrib.*',)
            ),
            OrderedAppList(
                _('Administration'),
                models = ('django.contrib.*',)
            ),
        ]

        if context['request'].user.is_superuser:
            self.children += [
                items.MenuItem(
                    _("Data exchange"),
                    children = [
                        items.MenuItem(_("Import data"), reverse('admin:index')),
                        items.MenuItem(_("Export data"), reverse('admin:index')),
                    ]
                ),
                items.MenuItem(
                    _("Advanced"),
                    children = [
                        items.MenuItem(_("Clear cache"), reverse('admin:index')),
                        items.MenuItem(_("Aggregates rebuilding"), reverse('admin:index')),
                        items.MenuItem(_("Mail server test"), reverse('admin:index')),
                        items.MenuItem(_("SMS gateway test"), reverse('admin:index')),
                        items.MenuItem(_("Test view"), reverse('admin:index')),
                        items.MenuItem(_("Debug view"), reverse('admin:index')),
                        items.MenuItem(_("Server reset"), reverse('admin:index')),
                    ]
                ),
            ]

        self.children += [
            items.Bookmarks(),
        ]
