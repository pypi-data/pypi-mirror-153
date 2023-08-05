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

"""PyAMS_*** module

"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_file.property import FileProperty
from pyams_security_views.interfaces.login import ILoginConfiguration
from pyams_site.interfaces import ISiteEtcTraverser, ISiteRoot
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'


@factory_config(ILoginConfiguration)
class LoginConfiguration(Persistent, Contained):
    """Site login configuration"""

    logo = FileProperty(ILoginConfiguration['logo'])
    header = FieldProperty(ILoginConfiguration['header'])
    header_renderer = FieldProperty(ILoginConfiguration['header_renderer'])
    footer = FieldProperty(ILoginConfiguration['footer'])
    footer_renderer = FieldProperty(ILoginConfiguration['footer_renderer'])


LOGIN_CONFIGURATION_KEY = 'pyams_security.login.configuration'
"""Annotations key used to store login configuration"""


@adapter_config(required=ISiteRoot, provides=ILoginConfiguration)
def site_root_login_configuration_factory(context):
    """Site root login configuration factory"""
    return get_annotation_adapter(context, LOGIN_CONFIGURATION_KEY, ILoginConfiguration,
                                  name='++etc++login.configuration')


@adapter_config(name='login.configuration', required=ISiteRoot, provides=ISiteEtcTraverser)
def site_root_login_configuration_traverser(context):
    """Site root ++etc++login.configuration traverser extension"""
    return ILoginConfiguration(context, None)
