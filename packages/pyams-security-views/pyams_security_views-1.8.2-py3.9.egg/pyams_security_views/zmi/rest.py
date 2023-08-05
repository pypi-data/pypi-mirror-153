#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_security_views.zmi.rest module

This module defines components which are used to handle REST security configuration
to set allowed CORS origins.
"""

from zope.interface import Interface

from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import MANAGE_SECURITY_PERMISSION
from pyams_security.interfaces.rest import ICORSSecurityInfo
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

from pyams_security_views import _


@viewlet_config(name='cors-configuration.menu',
                context=ISecurityManager, layer=IAdminLayer,
                manager=ISecurityMenu, weight=20,
                permission=MANAGE_SECURITY_PERMISSION)
class CORSConfigurationMenu(NavigationMenuItem):
    """CORS configuration menu"""

    label = _("CORS configuration")
    href = '#cors-configuration.html'


@ajax_form_config(name='cors-configuration.html',
                  context=ISecurityManager, layer=IPyAMSLayer,
                  permission=MANAGE_SECURITY_PERMISSION)
class CORSConfigurationEditForm(AdminEditForm):
    """CORS configuration edit form"""

    title = _("CORS configuration")

    fields = Fields(Interface)

    def get_content(self):
        """Content getter"""
        return get_utility(ISecurityManager)


@adapter_config(name='cors-configuration',
                required=(ISecurityManager, IAdminLayer, CORSConfigurationEditForm),
                provides=IGroup)
class CORSConfigurationGroup(FormGroupChecker):
    """CORS configuration group"""

    fields = Fields(ICORSSecurityInfo)

    label_css_class = 'col-sm-2 col-md-3'
    input_css_class = 'col-sm-10 col-md-9'

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        origins = self.widgets.get('allowed_origins')
        if origins is not None:
            origins.rows = 10


@viewlet_config(name='cors-configuration.header',
                context=ISecurityManager, layer=IAdminLayer, view=CORSConfigurationGroup,
                manager=IHeaderViewletManager, weight=1)
class CORSConfigurationHeader(AlertMessage):
    """CORS configuration header"""

    status = 'info'

    _message = _("If you disable CORS origins check, any CORS request will be accepted.\n"
                 "Otherwise, only origins specified below will be allowed.\n"
                 "Please note that you don't have to set main site URL(s) below, only "
                 "\"external\" URLs have to be defined.")
