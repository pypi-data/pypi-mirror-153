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

"""PyAMS_security_views.zmi.login module

This module provides views and content providers used to manage login page configuration.
"""

from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import MANAGE_SYSTEM_PERMISSION
from pyams_security_views.interfaces.login import ILoginConfiguration
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.helper.event import get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.interfaces import IConfigurationMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_security_views import _  # pylint: disable=ungrouped-imports


@viewletmanager_config(name='login-form-configuration.menu', context=ISiteRoot, layer=IAdminLayer,
                       manager=IConfigurationMenu, weight=20,
                       permission=MANAGE_SYSTEM_PERMISSION)
class LoginFormConfigurationMenu(NavigationMenuItem):
    """Login form configuration menu"""

    label = _("Login form")
    href = '#login-form-configuration.html'


@ajax_form_config(name='login-form-configuration.html', context=ISiteRoot, layer=IPyAMSLayer,
                  permission=MANAGE_SYSTEM_PERMISSION)
class LoginFormConfigurationForm(AdminEditForm):
    """Login form configuration form"""

    title = _("Login form configuration")
    legend = _("Form properties")

    fields = Fields(ILoginConfiguration)

    def get_content(self):
        return ILoginConfiguration(self.context)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if 'header' in self.widgets:
            self.widgets['header'].set_widgets_attr('rows', 5)
            self.widgets['header'].add_widgets_class('monospace')
        if 'footer' in self.widgets:
            self.widgets['footer'].set_widgets_attr('rows', 5)
            self.widgets['footer'].add_widgets_class('monospace')


@adapter_config(required=(ISiteRoot, IAdminLayer, LoginFormConfigurationForm),
                provides=IAJAXFormRenderer)
class LoginFormConfigurationRenderer(ContextRequestViewAdapter):
    """Login form configuration form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes and ('logo' in changes.get(ILoginConfiguration, ())):
            return get_json_widget_refresh_callback(self.view, 'logo', self.request)
        return None
