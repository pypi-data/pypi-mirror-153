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

"""PyAMS_security_views.zmi.manager module

This module provides views and content providers used to manage security manager properties.
"""

from zope.interface import Interface, implementer

from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup, IInnerSubForm
from pyams_form.subform import InnerEditForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import MANAGE_SECURITY_PERMISSION
from pyams_security_views.zmi import ISecurityMenu
from pyams_security_views.zmi.interfaces import ISecurityPropertiesEditForm
from pyams_security_views.zmi.widget import SecurityManagerPluginsFieldWidget
from pyams_skin.interfaces.viewlet import IHeaderViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_security_views import _  # pylint: disable=ungrouped-imports


@adapter_config(required=(ISecurityManager, IAdminLayer, Interface),
                provides=IObjectLabel)
def security_manager_label(context, request, view):
    """Security manager label getter"""
    return request.localizer.translate(_("Security manager"))


@viewlet_config(name='security-properties.menu',
                context=ISecurityManager, layer=IAdminLayer,
                manager=ISecurityMenu, weight=10,
                permission=MANAGE_SECURITY_PERMISSION)
class SecurityPropertiesMenu(NavigationMenuItem):
    """Security manager properties menu"""

    label = _("Properties")
    href = '#security-properties.html'


@ajax_form_config(name='security-properties.html',
                  context=ISecurityManager, layer=IPyAMSLayer,
                  permission=MANAGE_SECURITY_PERMISSION)
@implementer(ISecurityPropertiesEditForm)
class SecurityPropertiesEditForm(AdminEditForm):
    """Security manager properties edit form"""

    title = _("Security manager")
    legend = _("Properties")

    fields = Fields(ISecurityManager).select('credentials_plugins_names',
                                             'authentication_plugins_names',
                                             'directory_plugins_names')
    fields['credentials_plugins_names'].widget_factory = SecurityManagerPluginsFieldWidget
    fields['authentication_plugins_names'].widget_factory = SecurityManagerPluginsFieldWidget
    fields['directory_plugins_names'].widget_factory = SecurityManagerPluginsFieldWidget


@adapter_config(name='security-registration',
                required=(ISecurityManager, IAdminLayer, SecurityPropertiesEditForm),
                provides=IGroup)
class SecurityRegistrationGroup(FormGroupChecker):
    """Security manager registration fields"""

    fields = Fields(ISecurityManager).select('open_registration', 'users_folder')


@viewlet_config(name='security-registration.header',
                context=ISecurityManager, layer=IAdminLayer, view=SecurityRegistrationGroup,
                manager=IHeaderViewletManager, weight=1)
class SecurityRegistrationHeader(AlertMessage):
    """Security registration header"""

    status = 'info'

    _message = _("Open registration can be used when you want external users to be able to "
                 "freely register their user account.\n"
                 "You then have to select the users folder into which their profile will be "
                 "stored.\n"
                 "THIS CAN BE DANGEROUS! You should enable this feature carefully...")


@adapter_config(name='security-zmi',
                required=(ISecurityManager, IAdminLayer, SecurityPropertiesEditForm),
                provides=IInnerSubForm)
class SecurityZMIEditForm(InnerEditForm):
    """Security manager administration interface edit form"""

    legend = _("Management interface")

    fields = Fields(ISecurityManager).select('show_home_menu')
