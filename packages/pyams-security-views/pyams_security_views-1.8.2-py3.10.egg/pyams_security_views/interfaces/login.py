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

from zope.interface import Interface
from zope.schema import Choice, Password, TextLine

from pyams_file.schema import ImageField
from pyams_i18n.schema import I18nTextField
from pyams_skin.schema.button import CloseButton, ResetButton, SubmitButton
from pyams_utils.text import PYAMS_HTML_RENDERERS_VOCABULARY


__docformat__ = 'restructuredtext'

from pyams_security_views import _


class ILoginConfiguration(Interface):
    """Login configuration interface"""

    logo = ImageField(title=_("Login logo"),
                      description=_("Image used in login form"),
                      required=False)

    header = I18nTextField(title=_("Login header"),
                           description=_("This text will be displayed in login page header"),
                           required=False)

    header_renderer = Choice(title=_("Header renderer"),
                             description=_("Text renderer used for the header"),
                             required=True,
                             vocabulary=PYAMS_HTML_RENDERERS_VOCABULARY,
                             default='text')

    footer = I18nTextField(title=_("Login footer"),
                           description=_("This text will be displayed in login page footer"),
                           required=False)

    footer_renderer = Choice(title=_("Footer renderer"),
                             description=_("Text renderer used for the footer"),
                             required=True,
                             vocabulary=PYAMS_HTML_RENDERERS_VOCABULARY,
                             default='text')


class ILoginView(Interface):
    """Login view marker interface"""


class ILoginFormFields(Interface):
    """Login form fields"""

    hash = TextLine(title=_("Redirection hash"),
                    required=False)

    login = TextLine(title=_("Login"))

    password = Password(title=_("Password"))


class ILoginFormButtons(Interface):
    """Login form buttons"""

    login = SubmitButton(name='login',
                         title=_("Connect"))

    reset = ResetButton(name='reset',
                        title=_("Reset"))


class IModalLoginFormButtons(Interface):
    """Modal login form buttons"""

    login = SubmitButton(name='login',
                         title=_("Connect"))

    close = CloseButton(name='close',
                        title=_("Cancel"))
