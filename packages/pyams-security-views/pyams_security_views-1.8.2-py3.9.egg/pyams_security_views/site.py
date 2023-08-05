#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_security_views.site module

This module provides a default security context from site root.
"""

from zope.interface import Interface

from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_security.interfaces.base import MANAGE_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config


__docformat__ = 'restructuredtext'


@adapter_config(required=(ISiteRoot, IPyAMSLayer, Interface),
                provides=IViewContextPermissionChecker)
class SiteRootPermissionChecker(ContextRequestViewAdapter):
    """Site root permission checker"""

    edit_permission = MANAGE_SYSTEM_PERMISSION
