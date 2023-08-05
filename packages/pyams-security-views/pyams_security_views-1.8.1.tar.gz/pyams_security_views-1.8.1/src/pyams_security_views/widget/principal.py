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

"""PyAMS_security_views.widget.principal module

This module defines widgets to select principals.
"""

from zope.interface import implementer_only
from zope.schema.vocabulary import SimpleTerm

from pyams_form.browser.select import SelectWidget
from pyams_form.converter import SequenceDataConverter
from pyams_form.interfaces import IDataConverter
from pyams_form.interfaces.widget import IFieldWidget
from pyams_form.widget import FieldWidget
from pyams_layer.interfaces import IFormLayer
from pyams_security.interfaces import ISecurityManager
from pyams_security.schema import IPrincipalField, IPrincipalsSetField
from pyams_security_views.widget.interfaces import IPrincipalWidget, IPrincipalsSetWidget
from pyams_utils.adapter import adapter_config
from pyams_utils.registry import get_utility


__docformat__ = 'restructuredtext'

from pyams_security_views import _


def principal_term_factory(value):
    """Principal term factory"""
    manager = get_utility(ISecurityManager)
    principal = manager.get_principal(value)
    if principal is not None:
        return SimpleTerm(principal.id, title=principal.title)
    return None


#
# Principal widget
#

@adapter_config(required=(IPrincipalField, IPrincipalWidget),
                provides=IDataConverter)
class PrincipalDataConverter(SequenceDataConverter):
    """Principal data converter"""

    def to_widget_value(self, value):
        """Value to widget converter"""
        if isinstance(value, set):
            try:
                value = next(iter(value))
            except StopIteration:
                value = None
        return super().to_widget_value(value)


@implementer_only(IPrincipalWidget)
class PrincipalWidget(SelectWidget):
    """Principal widget"""

    placeholder = _("No selected principal")
    separator = '|'

    ajax_url = '/api/security/principals'

    @staticmethod
    def term_factory(value):
        """Selected principals terms factory"""
        return principal_term_factory(value)


@adapter_config(required=(IPrincipalField, IFormLayer),
                provides=IFieldWidget)
def PrincipalFieldWidget(field, request):  # pylint: disable=invalid-name
    """Principal field widget factory"""
    return FieldWidget(field, PrincipalWidget(request))


#
# Principals set widget
#

@implementer_only(IPrincipalsSetWidget)
class PrincipalsSetWidget(PrincipalWidget):
    """Principals set widget"""

    multiple = 'multiple'


@adapter_config(required=(IPrincipalsSetField, IFormLayer),
                provides=IFieldWidget)
def PrincipalsSetFieldWidget(field, request):  # pylint: disable=invalid-name
    """Principals set field widget factory"""
    return FieldWidget(field, PrincipalsSetWidget(request))
