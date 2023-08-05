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

"""PyAMS_security_views.zmi.interfaces module

This module defines public views and viewlet managers interfaces.
"""

from zope.interface import Interface

from pyams_form.interfaces.form import IEditForm
from pyams_skin.interfaces.widget import IOrderedListWidget
from pyams_zmi.interfaces.viewlet import INavigationMenuItem


__docformat__ = 'restructuredtext'


class ISecurityMenu(INavigationMenuItem):
    """Security menu interface"""


class IObjectSecurityMenu(INavigationMenuItem):
    """Object security menu"""


class ISecurityManagerView(Interface):
    """Security manager view"""


class ISecurityPropertiesEditForm(IEditForm):
    """Security properties edit form marker interface"""


class ISecurityManagerPluginsWidget(IOrderedListWidget):
    """Security plugins ordering widget"""
