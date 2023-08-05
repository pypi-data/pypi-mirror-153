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

"""PyAMS_security_views.zmi.policy module

This module defines views and content providers which are used to manage roles and
security policy
"""

from zope.component import getAdapters
from zope.interface import Interface

from pyams_form.ajax import ajax_form_config
from pyams_form.browser.checkbox import SingleCheckBoxFieldWidget
from pyams_form.field import Fields
from pyams_form.interfaces import DISPLAY_MODE, INPUT_MODE
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import IDefaultProtectionPolicy, IProtectedObject, IRolesPolicy
from pyams_security.interfaces.base import IRole, MANAGE_SECURITY_PERMISSION, \
    VIEW_SYSTEM_PERMISSION
from pyams_security_views.zmi.interfaces import IObjectSecurityMenu
from pyams_skin.interfaces.viewlet import IHelpViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.registry import get_utility
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import ISiteManagementMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_security_views import _  # pylint: disable=ungrouped-imports


#
# Object roles views
#

@viewletmanager_config(name='object-roles.menu', context=IDefaultProtectionPolicy,
                       layer=IAdminLayer, manager=ISiteManagementMenu, weight=900,
                       permission=VIEW_SYSTEM_PERMISSION,
                       provides=IObjectSecurityMenu)
class ObjectSecurityMenu(NavigationMenuItem):
    """Object security menu"""

    label = _("User roles")
    icon_class = 'fas fa-users'
    href = '#object-roles.html'


@ajax_form_config(name='object-roles.html', context=IDefaultProtectionPolicy,
                  layer=IPyAMSLayer, permission=VIEW_SYSTEM_PERMISSION)
class ProtectedObjectRolesEditForm(AdminEditForm):
    """Protected object roles edit form"""

    title = _("User roles")
    legend = _("Granted object roles")

    @property
    def fields(self):
        """Form fields getter"""
        fields = Fields(Interface)
        for _name, policy in sorted(getAdapters((self.context,), IRolesPolicy),
                                    key=lambda x: x[1].weight):
            fields += Fields(policy.roles_interface)
        return fields

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if self.mode == DISPLAY_MODE:
            return
        principals = self.request.effective_principals
        for widget in self.widgets.values():
            widget.mode = DISPLAY_MODE
            role = get_utility(IRole, name=widget.field.role_id)
            if role.managers:
                for manager in role.managers:
                    if manager in principals:
                        widget.mode = INPUT_MODE
                        break


@viewlet_config(name='object-roles.alert', context=IDefaultProtectionPolicy,
                layer=IAdminLayer, view=ProtectedObjectRolesEditForm,
                manager=IHelpViewletManager, weight=1)
class ProtectedObjectRolesAlert(AlertMessage):
    """Protected object roles alert"""

    def __new__(cls, context, request, view, manager):  # pylint: disable=unused-argument
        if not view.widgets:
            return AlertMessage.__new__(cls)
        return None

    status = 'danger'
    _message = _("Roles are not defined for this context!")


#
# Security policy views
#

@viewlet_config(name='security-policy.menu', context=IDefaultProtectionPolicy,
                layer=IAdminLayer, manager=IObjectSecurityMenu,
                permission=MANAGE_SECURITY_PERMISSION, weight=10)
class ProtectedObjectSecurityPolicyMenuItem(NavigationMenuItem):
    """Protected object security policy menu item"""

    label = _("Security policy")
    icon_class = 'fas fa-key'
    href = '#security-policy.html'


@ajax_form_config(name='security-policy.html', context=IDefaultProtectionPolicy,
                  layer=IPyAMSLayer, permission=MANAGE_SECURITY_PERMISSION)
class ProtectedObjectSecurityPolicyEditForm(AdminEditForm):
    """Protected object security policy edit form"""

    title = _("Security manager")
    legend = _("Security policy management")

    fields = Fields(IProtectedObject)
    fields['inherit_parent_security'].widget_factory = SingleCheckBoxFieldWidget
    fields['inherit_parent_roles'].widget_factory = SingleCheckBoxFieldWidget

    def get_content(self):
        return IProtectedObject(self.context)
