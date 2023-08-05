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

"""PyAMS_security_views.widget.interfaces module

This module defines public interfaces of permissions and principals selection widgets.
"""

from pyams_form.interfaces.widget import ISelectWidget
from pyams_skin.interfaces.widget import IDynamicSelectWidget


__docformat__ = 'restructuredtext'


class IPermissionWidget(ISelectWidget):
    """Permission widget"""


class IPermissionsSetWidget(ISelectWidget):
    """Permissions set widget"""


class IPrincipalWidget(IDynamicSelectWidget):
    """Principal widget"""


class IPrincipalsSetWidget(IDynamicSelectWidget):
    """Principals set widget"""
