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

"""PyAMS_security_views.zmi.notifications module

This module provides notifications management views.
"""

from zope.interface import Interface

from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import MANAGE_SECURITY_PERMISSION
from pyams_security.interfaces.notification import INotificationSettings
from pyams_security_views.zmi import ISecurityMenu
from pyams_skin.interfaces.viewlet import IHeaderViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.adapter import adapter_config
from pyams_utils.registry import get_utility
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_security_views import _  # pylint: disable=ungrouped-imports


@viewlet_config(name='security-notifications.menu',
                context=ISecurityManager, layer=IAdminLayer,
                manager=ISecurityMenu, weight=15,
                permission=MANAGE_SECURITY_PERMISSION)
class SecurityNotificationsMenu(NavigationMenuItem):
    """Security manager notifications menu"""

    label = _("Notifications")
    href = '#security-notifications.html'


@ajax_form_config(name='security-notifications.html',
                  context=ISecurityManager, layer=IPyAMSLayer,
                  permission=MANAGE_SECURITY_PERMISSION)
class SecurityNotificationsEditForm(AdminEditForm):
    """Security notifications edit form"""

    title = _("Notifications settings")

    fields = Fields(Interface)

    def get_content(self):
        return get_utility(ISecurityManager)


@adapter_config(name='security-notifications',
                required=(ISecurityManager, IAdminLayer, SecurityNotificationsEditForm),
                provides=IGroup)
class SecurityNotificationsGroup(FormGroupChecker):
    """Security notifications settings group"""

    fields = Fields(INotificationSettings)


@viewlet_config(name='security-notifications.header',
                context=ISecurityManager, layer=IAdminLayer, view=SecurityNotificationsGroup,
                manager=IHeaderViewletManager, weight=1)
class SecurityNotificationsHeader(AlertMessage):
    """Security notifications header"""

    status = 'info'

    _message = _("Notifications are used to send messages to users during their registration "
                 "process.\n"
                 "Applications can also send messages during their normal process.")
