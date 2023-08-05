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

"""PyAMS_security_views.widget.permission module

This module defines widgets to select permissions.
"""

from zope.interface import implementer_only

from pyams_form.browser.select import SelectWidget
from pyams_form.converter import CollectionSequenceDataConverter
from pyams_form.interfaces import IDataConverter
from pyams_form.interfaces.widget import IFieldWidget
from pyams_form.widget import FieldWidget
from pyams_layer.interfaces import IFormLayer
from pyams_security.schema import IPermissionField, IPermissionsSetField
from pyams_security_views.widget.interfaces import IPermissionWidget, IPermissionsSetWidget
from pyams_utils.adapter import adapter_config


__docformat__ = 'restructuredtext'


#
# Permission widget
#

@implementer_only(IPermissionWidget)
class PermissionWidget(SelectWidget):
    """Principal widget"""


@adapter_config(required=(IPermissionField, IFormLayer),
                provides=IFieldWidget)
def PermissionFieldWidget(field, request):  # pylint: disable=invalid-name
    """Permission field widget factory"""
    return FieldWidget(field, PermissionWidget(request))


#
# Permissions set widget
#

@adapter_config(required=(IPermissionsSetField, IPermissionsSetWidget),
                provides=IDataConverter)
class PermissionsSetDataConverter(CollectionSequenceDataConverter):
    """Permissions set data converter"""


@implementer_only(IPermissionsSetWidget)
class PermissionsSetWidget(SelectWidget):
    """Permissions set widget"""

    multiple = True


@adapter_config(required=(IPermissionsSetField, IFormLayer),
                provides=IFieldWidget)
def PermissionsSetFieldWidget(field, request):  # pylint: disable=invalid-name
    """Permissions set field widget factory"""
    return FieldWidget(field, PermissionsSetWidget(request))
