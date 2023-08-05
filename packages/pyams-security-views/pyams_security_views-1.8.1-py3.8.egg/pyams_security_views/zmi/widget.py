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

"""PyAMS_security_views.zmi.widget module

This modules defines widgets which are used to display security plug-ins.
"""

__docformat__ = 'restructuredtext'

from pyramid.decorator import reify
from zope.interface import implementer_only
from zope.schema.interfaces import ITuple
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_form.interfaces import ITerms
from pyams_form.term import Terms
from pyams_form.widget import FieldWidget
from pyams_security.interfaces import IPlugin, ISecurityManager
from pyams_security_views.zmi.interfaces import ISecurityManagerPluginsWidget, \
    ISecurityPropertiesEditForm
from pyams_skin.widget.list import OrderedListWidget
from pyams_utils.adapter import adapter_config
from pyams_utils.registry import query_utility
from pyams_zmi.interfaces import IAdminLayer


@implementer_only(ISecurityManagerPluginsWidget)
class SecurityManagerPluginsWidget(OrderedListWidget):
    """Security manager plugins widget"""


def SecurityManagerPluginsFieldWidget(field, request):  # pylint: disable=invalid-name
    """Security manager plugins field widget"""
    return FieldWidget(field, SecurityManagerPluginsWidget(request))


@adapter_config(required=(ISecurityManager, IAdminLayer, ISecurityPropertiesEditForm,
                          ITuple, ISecurityManagerPluginsWidget),
                provides=ITerms)
class SecurityManagerPluginsTerms(Terms):
    """Security manager plugins terms"""

    def __init__(self, context, request, form, field, widget):  # pylint: disable=too-many-arguments
        self.context = context
        self.request = request
        self.form = form
        self.field = field
        self.widget = widget

    @reify
    def terms(self):
        """Inner terms getter"""
        field = self.field.bind(self.context)
        terms = []
        for name in field.get(self.context):
            plugin = query_utility(IPlugin, name=name)
            if plugin is None:
                plugin = self.context.get(name)
            if plugin is not None:
                terms.append(SimpleTerm(name,
                                        title=self.request.localizer.translate(plugin.title)))
        return SimpleVocabulary(terms)
