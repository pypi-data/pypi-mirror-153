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

"""PyAMS_security_views.zmi.plugin.admin module

Internal authentication plug-ins management views.
"""

from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import MANAGE_SECURITY_PERMISSION
from pyams_security.interfaces.plugin import ADMIN_AUTHENTICATION_PLUGIN_LABEL, \
    IAdminAuthenticationPlugin
from pyams_security_views.zmi import SecurityPluginsTable
from pyams_security_views.zmi.plugin import SecurityPluginAddForm, SecurityPluginAddMenu, \
    SecurityPluginPropertiesEditForm
from pyams_skin.interfaces.viewlet import IHelpViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager


__docformat__ = 'restructuredtext'

from pyams_security_views import _  # pylint: disable=ungrouped-imports


@viewlet_config(name='add-admin-authentication-plugin.menu',
                context=ISecurityManager, layer=IAdminLayer, view=SecurityPluginsTable,
                manager=IContextAddingsViewletManager, weight=10,
                permission=MANAGE_SECURITY_PERMISSION)
class AdminAuthenticationPluginAddMenu(SecurityPluginAddMenu):
    """Admin authentication plug-in add menu"""

    label = _("Add admin authentication...")
    href = 'add-admin-authentication-plugin.html'


@ajax_form_config(name='add-admin-authentication-plugin.html',
                  context=ISecurityManager, layer=IPyAMSLayer,
                  permission=MANAGE_SECURITY_PERMISSION)
class AdminAuthenticationPluginAddForm(SecurityPluginAddForm):
    """Admin authentication plug-in add form"""

    content_factory = IAdminAuthenticationPlugin
    content_label = ADMIN_AUTHENTICATION_PLUGIN_LABEL


@ajax_form_config(name='properties.html',
                  context=IAdminAuthenticationPlugin, layer=IPyAMSLayer)
class AdminAuthenticationPluginPropertiesEditForm(SecurityPluginPropertiesEditForm):
    """Admin authentication plug-in properties editor adapter"""

    plugin_interface = IAdminAuthenticationPlugin

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if 'password' in self.widgets:
            alert = AdminAuthenticationPluginPasswordAlert(self.context, self.request, self, None)
            self.widgets['password'].suffix = alert
            self.widgets['password'].autocomplete = 'new-password'


@viewlet_config(name='properties.help', context=IAdminAuthenticationPlugin,
                layer=IAdminLayer, view=AdminAuthenticationPluginPropertiesEditForm,
                manager=IHelpViewletManager)
class AdminAuthenticationPluginPropertiesAlertMessage(AlertMessage):
    """Admin authentication plug-in properties alert message"""

    status = 'danger'
    icon_class = 'fas fa-exclamation-triangle'
    header = _("Warning!")
    _message = _("Before disabling plug-in, you should verify that you have other administration "
                 "access!")


class AdminAuthenticationPluginPasswordAlert(AlertMessage):
    """Admin authentication plug-in password alert message"""

    status = 'warning'
    css_class = 'mt-1 p-2'
    _message = _("<strong>Be careful to redefine the password when using some browsers which "
                 "are forcing autocompletion!!!</strong><br />"
                 "Clearing the password will keep the plug-in active but without the option "
                 "to log-in with this account; setting the password value to '*****' will leave "
                 "the password as-is...")
    message_renderer = 'raw'
