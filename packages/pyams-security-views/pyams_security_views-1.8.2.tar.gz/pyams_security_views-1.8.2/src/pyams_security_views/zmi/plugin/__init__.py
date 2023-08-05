#
# Copyright (c) 2015-2020 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_security_views.zmi.plugin base module

This module defines classes which are used by all security plug-ins management views.
"""

from pyramid.events import subscriber
from zope.interface import Interface, Invalid

from pyams_form.browser.checkbox import SingleCheckBoxFieldWidget
from pyams_form.field import Fields
from pyams_form.interfaces import DISPLAY_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent
from pyams_security.interfaces import IPlugin, ISecurityManager, IViewContextPermissionChecker
from pyams_security.interfaces.base import MANAGE_SECURITY_PERMISSION
from pyams_security_views.zmi import SecurityPluginsTable
from pyams_skin.viewlet.menu import MenuItem
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.event import get_json_table_row_add_callback, \
    get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_label


__docformat__ = 'restructuredtext'

from pyams_security_views import _  # pylint: disable=ungrouped-imports


class SecurityPluginAddMenu(MenuItem):
    """Security manager plug-in add form"""

    modal_target = True

    def get_href(self):
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        return absolute_url(sm, self.request, self.href)


class SecurityPluginAddForm(AdminModalAddForm):
    """Security plug-in add form"""

    @property
    def title(self):
        """Add form title getter"""
        translate = self.request.localizer.translate
        return '<small>{}</small><br />{}'.format(
            get_object_label(self.context, self.request, self),
            translate(_("New plug-in: {}")).format(translate(self.content_label)))

    legend = _("New plug-in properties")
    content_factory = IPlugin
    content_label = '--'

    object_data = {
        'ams-warn-on-change': False
    }

    @property
    def fields(self):
        """Form fields getter"""
        fields = Fields(self.content_factory).omit('__parent__', '__name__')
        fields['enabled'].widget_factory = SingleCheckBoxFieldWidget
        return fields

    def add(self, obj):
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        sm[obj.prefix] = obj

    def next_url(self):
        return absolute_url(self.context, self.request, 'admin#security-plugins.html')


@subscriber(IDataExtractedEvent, form_selector=SecurityPluginAddForm)
def extract_plugin_add_form_data(event):
    """Security plug-in add form data extraction"""
    data = event.data
    sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
    if data.get('prefix') in sm:
        event.form.widgets.errors += (Invalid(_("Specified prefix is already used!")),)


@adapter_config(required=(ISecurityManager, IAdminLayer, SecurityPluginAddForm),
                provides=IAJAXFormRenderer)
class SecurityPluginAddFormRenderer(ContextRequestViewAdapter):
    """Security plug-in add form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:  # WARNING: creating an empty container will return a "false" value!
            return None
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        return {
            'callbacks': [
                get_json_table_row_add_callback(sm, self.request,
                                                SecurityPluginsTable, changes)
            ]
        }


@adapter_config(required=IPlugin,
                provides=IObjectLabel)
def security_plugin_label(context):
    """Security plug-in name adapter"""
    return context.title


class InnerSecurityPluginFormMixin:
    """Inner security plug-in form mixin"""

    @property
    def title(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        manager = get_utility(ISecurityManager)
        plugin = get_parent(self.context, IPlugin)
        return '<small>{}</small><br />{}'.format(
            get_object_label(manager, self.request, self),
            translate(_("Plug-in: {}")).format(get_object_label(plugin, self.request, self)))


@adapter_config(required=(IPlugin, IAdminLayer, Interface),
                provides=ITableElementEditor)
class SecurityPluginEditor(TableElementEditor):
    """Security plug-in editor adapter"""


@adapter_config(required=IPlugin, provides=IViewContextPermissionChecker)
class SecurityManagerPluginPermissionChecker(ContextAdapter):
    """Security manager plug-in permission checker"""

    edit_permission = MANAGE_SECURITY_PERMISSION


class SecurityPluginPropertiesEditForm(AdminModalEditForm):
    """Security plug-in properties editor adapter"""

    @property
    def title(self):
        """Plug-in edit form title getter"""
        translate = self.request.localizer.translate
        manager = get_utility(ISecurityManager)
        plugin = get_parent(self.context, IPlugin)
        return '<small>{}</small><br />{}'.format(
            get_object_label(manager, self.request, self),
            translate(_("Plug-in: {}")).format(get_object_label(plugin, self.request, self)))

    legend = _("Plug-in properties")

    plugin_interface = IPlugin
    content_label = '--'

    @property
    def fields(self):
        """Form fields getter"""
        fields = Fields(self.plugin_interface).omit('__parent__', '__name__')
        fields['enabled'].widget_factory = SingleCheckBoxFieldWidget
        return fields

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if 'prefix' in self.widgets:
            self.widgets['prefix'].mode = DISPLAY_MODE


@adapter_config(required=(IPlugin, IAdminLayer, SecurityPluginPropertiesEditForm),
                provides=IAJAXFormRenderer)
class SecurityPluginPropertiesAJAXRenderer(ContextRequestViewAdapter):
    """Security plugin properties AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        return get_json_table_row_refresh_callback(sm, self.request,
                                                   SecurityPluginsTable, self.context)
