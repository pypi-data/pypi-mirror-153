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

"""PyAMS_security_views.zmi.plugin.userfolder module

Local users management views.
"""

from datetime import datetime
from pyramid.events import subscriber
from pyramid.view import view_config
from zope.interface import Interface, Invalid

from pyams_form.ajax import ajax_form_config
from pyams_form.browser.checkbox import SingleCheckBoxFieldWidget
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.interfaces import DISPLAY_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces import ISecurityManager, IViewContextPermissionChecker
from pyams_security.interfaces.base import MANAGE_SECURITY_PERMISSION
from pyams_security.interfaces.plugin import ILocalUser, IUsersFolderPlugin, \
    USERS_FOLDER_PLUGIN_LABEL
from pyams_security_views.zmi import SecurityPluginsTable
from pyams_security_views.zmi.plugin import InnerSecurityPluginFormMixin, SecurityPluginAddForm, \
    SecurityPluginAddMenu, SecurityPluginPropertiesEditForm
from pyams_skin.schema.button import ActionButton, SubmitButton
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.container import delete_container_element
from pyams_zmi.helper.event import get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IModalDisplayFormButtons, IModalEditFormButtons
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IToolbarViewletManager
from pyams_zmi.search import SearchForm, SearchResultsView, SearchView
from pyams_zmi.table import I18nColumnMixin, IconColumn, Table, TableElementEditor, TrashColumn


__docformat__ = 'restructuredtext'

from pyams_security_views import _  # pylint: disable=ungrouped-imports


@viewlet_config(name='add-users-folder-plugin.menu',
                context=ISecurityManager, layer=IAdminLayer, view=SecurityPluginsTable,
                manager=IContextAddingsViewletManager, weight=20,
                permission=MANAGE_SECURITY_PERMISSION)
class UsersFolderPluginAddMenu(SecurityPluginAddMenu):
    """Users folder plug-in add menu"""

    label = _("Add local users folder...")
    href = 'add-users-folder-plugin.html'


@ajax_form_config(name='add-users-folder-plugin.html',
                  context=ISecurityManager, layer=IPyAMSLayer,
                  permission=MANAGE_SECURITY_PERMISSION)
class UsersFolderPluginAddForm(SecurityPluginAddForm):
    """Users folder plug-in add form"""

    content_factory = IUsersFolderPlugin
    content_label = USERS_FOLDER_PLUGIN_LABEL


@ajax_form_config(name='properties.html',
                  context=IUsersFolderPlugin, layer=IPyAMSLayer)
class UsersFolderPropertiesEditForm(SecurityPluginPropertiesEditForm):
    """Users folder plug-in properties edit form"""

    plugin_interface = IUsersFolderPlugin


#
# Local users folder search view
#

class LocalUsersSearchForm(SearchForm):  # pylint: disable=abstract-method
    """Local users search form"""

    title = _("Users search form")

    @property
    def back_url(self):
        """Form back URL getter"""
        manager = get_utility(ISecurityManager)
        return absolute_url(manager, self.request, 'security-plugins.html')


@pagelet_config(name='search.html', context=IUsersFolderPlugin, layer=IPyAMSLayer,
                permission=MANAGE_SECURITY_PERMISSION)
class LocalUsersSearchView(SearchView):
    """Local users search view"""

    title = _("Users search form")
    search_form = LocalUsersSearchForm


class LocalUsersSearchResultsTable(Table):
    """Local users search results table"""


@adapter_config(required=(IUsersFolderPlugin, IAdminLayer, LocalUsersSearchResultsTable),
                provides=IValues)
class LocalUsersSearchResultsValues(ContextRequestViewAdapter):
    """Local users search results values"""

    @property
    def values(self):
        """Local users search table results getter"""
        yield from self.context.get_search_results({
            'query': self.request.params.get('form.widgets.query')
        })


@adapter_config(name='login',
                required=(IUsersFolderPlugin, IAdminLayer, LocalUsersSearchResultsTable),
                provides=IColumn)
class LocalUsersSearchLoginColumn(I18nColumnMixin, GetAttrColumn):
    """Local users search login column"""

    i18n_header = _("Login")
    attr_name = 'login'

    weight = 10


@adapter_config(name='title',
                required=(IUsersFolderPlugin, IAdminLayer, LocalUsersSearchResultsTable),
                provides=IColumn)
class LocalUsersSearchTitleColumn(I18nColumnMixin, GetAttrColumn):
    """Local users search title column"""

    i18n_header = _("Title")
    attr_name = 'title'

    weight = 20


@adapter_config(name='email',
                required=(IUsersFolderPlugin, IAdminLayer, LocalUsersSearchResultsTable),
                provides=IColumn)
class LocalUsersSearchEmailColumn(I18nColumnMixin, GetAttrColumn):
    """Local users search email column"""

    i18n_header = _("Mail address")
    attr_name = 'email'

    weight = 30


@adapter_config(name='password',
                required=(IUsersFolderPlugin, IAdminLayer, LocalUsersSearchResultsTable),
                provides=IColumn)
class LocalUsersSearchPasswordColumn(IconColumn):
    """Local users search password column"""

    hint = _("Account has password set")
    icon_class = 'fas fa-key'

    weight = 180

    @staticmethod
    def checker(item):
        """Password column checker"""
        return item.password


@adapter_config(name='active',
                required=(IUsersFolderPlugin, IAdminLayer, LocalUsersSearchResultsTable),
                provides=IColumn)
class LocalUsersSearchActiveColumn(IconColumn):
    """Local users search active column"""

    hint = _("Account is activated")
    icon_class = 'fa fa-check'

    weight = 200

    @staticmethod
    def checker(item):
        """Active column checker"""
        return item.activated


@adapter_config(name='trash',
                required=(IUsersFolderPlugin, IAdminLayer, LocalUsersSearchResultsTable),
                provides=IColumn)
class LocalUsersSearchTrashColumn(TrashColumn):
    """Local users search trash column"""


@pagelet_config(name='search-results.html', context=IUsersFolderPlugin, layer=IPyAMSLayer,
                permission=MANAGE_SECURITY_PERMISSION, xhr=True)
class LocalUsersSearchResultsView(SearchResultsView):
    """Local users search results view"""

    table_label = _("Search results")
    table_class = LocalUsersSearchResultsTable


@view_config(name='delete-element.json', context=IUsersFolderPlugin, request_type=IPyAMSLayer,
             permission=MANAGE_SECURITY_PERMISSION, renderer='json', xhr=True)
def delete_local_user(request):
    """Local user delete view"""
    return delete_container_element(request)


#
# Local user views
#

@viewlet_config(name='add-user.action', context=IUsersFolderPlugin, layer=IAdminLayer,
                view=LocalUsersSearchForm, manager=IToolbarViewletManager, weight=10,
                permission=MANAGE_SECURITY_PERMISSION)
class LocalUserAddAction(ContextAddAction):
    """Local user add action"""

    label = _("Add user")
    href = 'add-user.html'


@ajax_form_config(name='add-user.html', context=IUsersFolderPlugin, layer=IPyAMSLayer,
                  permission=MANAGE_SECURITY_PERMISSION)
class LocalUserAddForm(InnerSecurityPluginFormMixin, AdminModalAddForm):
    """Local user add form"""

    legend = _("Add local user")

    fields = Fields(ILocalUser).select('login', 'email', 'firstname', 'lastname',
                                       'company_name', 'password_manager', 'password',
                                       'confirmed_password', 'wait_confirmation')
    fields['wait_confirmation'].widget_factory = SingleCheckBoxFieldWidget

    content_factory = ILocalUser

    def update_content(self, obj, data):
        data = data.get(self, {})
        for attr in ('login', 'email', 'firstname', 'lastname', 'company_name',
                     'password_manager', 'password', 'wait_confirmation'):
            setattr(obj, attr, data.get(attr))
        obj.self_registered = False
        if obj.wait_confirmation:
            obj.generate_secret()
        else:
            obj.activation_date = tztime(datetime.utcnow())
            obj.activated = True

    def add(self, obj):
        self.context[obj.login] = obj


@subscriber(IDataExtractedEvent, form_selector=LocalUserAddForm)
def extract_local_user_add_form_data(event):
    """Check new local user form data"""
    data = event.data
    folder = event.form.context
    if not folder.check_login(data.get('login')):
        event.form.widgets.errors += (Invalid(_("Specified login is already used.")),)
    password = data.get('password')
    if password and (password != data.get('confirmed_password')):
        event.form.widgets.errors += (Invalid(_("User password was not confirmed correctly.")),)


@adapter_config(required=(IUsersFolderPlugin, IAdminLayer, LocalUserAddForm),
                provides=IAJAXFormRenderer)
class LocalUserAddFormRenderer(ContextRequestViewAdapter):
    """Local user add form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'status': 'success',
            'message': self.request.localizer.translate(_("New user was created "
                                                          "successfully!"))
        }


class ILocalUserEditFormButtons(IModalEditFormButtons):
    """Local user edit form buttons"""

    change_password = ActionButton(name='change_password',
                                   title=_("Change password"))

    refresh = SubmitButton(name='refresh',
                           title=_("Refresh secret"))

    enable = SubmitButton(name='enable',
                          title=_("Enable"),
                          condition=lambda form: not form.context.activated)

    disable = SubmitButton(name='disable',
                           title=_("Disable"),
                           condition=lambda form: form.context.activated)


@ajax_form_config(name='properties.html', context=ILocalUser, layer=IPyAMSLayer)
class LocalUserEditForm(InnerSecurityPluginFormMixin, AdminModalEditForm):
    """Local user edit form"""

    @property
    def title(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        return '{}<br /><small>{}</small>'.format(
            super().title,
            translate(_("User: {}")).format(self.context.title))

    legend = _("User properties")

    fields = Fields(ILocalUser).omit('__parent__', '__name__', 'password', 'confirmed_password',
                                     'password_manager')
    fields['wait_confirmation'].widget_factory = SingleCheckBoxFieldWidget
    fields['self_registered'].widget_factory = SingleCheckBoxFieldWidget
    fields['activated'].widget_factory = SingleCheckBoxFieldWidget

    @property
    def buttons(self):
        if self.mode == DISPLAY_MODE:
            return Buttons(IModalDisplayFormButtons)
        return Buttons(ILocalUserEditFormButtons).select('change_password', 'apply',
                                                         'refresh', 'enable', 'disable',
                                                         'close')

    ajax_form_target = None

    def update_actions(self):
        super().update_actions()
        translate = self.request.localizer.translate
        if 'change_password' in self.actions:
            action = self.actions['change_password']
            action.add_class('btn-info mr-auto')
            action.href = absolute_url(self.context, self.request, 'change-password.html')
            action.modal_target = True
        if 'refresh' in self.actions:
            action = self.actions['refresh']
            action.add_class('btn-secondary')
            action.hint = translate(_("Refresh activation secret and send a new activation link "
                                      "to this user"))
        if 'enable' in self.actions:
            action = self.actions['enable']
            action.add_class('btn-secondary')
            action.hint = translate(_("Re-enable user profile"))
        if 'disable' in self.actions:
            action = self.actions['disable']
            action.add_class('btn-danger')
            action.hint = translate(_("Disable user profile temporarily will forbid login with "
                                      "this account..."))

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if ('wait_confirmation' in self.widgets) and self.context.activated:
            self.widgets['wait_confirmation'].mode = DISPLAY_MODE
        if 'activation_secret' in self.widgets:
            self.widgets['activation_secret'].mode = DISPLAY_MODE
        if 'activation_hash' in self.widgets:
            self.widgets['activation_hash'].mode = DISPLAY_MODE
        if 'activated' in self.widgets:
            self.widgets['activated'].mode = DISPLAY_MODE
        if 'activation_date' in self.widgets:
            self.widgets['activation_date'].mode = DISPLAY_MODE

    @handler(ILocalUserEditFormButtons['apply'])
    def handle_apply(self, action):
        super().handle_apply(self, action)  # pylint: disable=too-many-function-args

    @handler(ILocalUserEditFormButtons['refresh'])
    def handle_refresh(self, action):
        """Refresh button handler"""
        user = self.context
        user.refresh_secret(notify=True, request=self.request)
        self.finished_state.update({
            'action': action,
            'changes': user
        })

    @handler(ILocalUserEditFormButtons['enable'])
    def handle_enable(self, action):
        """Enable button handler"""
        user = self.get_content()
        user.wait_confirmation = False
        user.activated = True
        self.finished_state.update({
            'action': action,
            'changes': user
        })

    @handler(ILocalUserEditFormButtons['disable'])
    def handle_disable(self, action):
        """Disable button handler"""
        user = self.get_content()
        user.activated = False
        self.finished_state.update({
            'action': action,
            'changes': user
        })


@adapter_config(name='apply',
                required=(ILocalUser, IAdminLayer, LocalUserEditForm),
                provides=IAJAXFormRenderer)
class LocalUserEditFormApplyActionRenderer(ContextRequestViewAdapter):
    """Local user edit form 'apply' action renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        folder = get_parent(self.context, IUsersFolderPlugin)
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(folder, self.request,
                                                    LocalUsersSearchResultsTable, self.context)
            ]
        }


@adapter_config(name='refresh',
                required=(ILocalUser, IAdminLayer, LocalUserEditForm),
                provides=IAJAXFormRenderer)
class LocalUserEditFormRefreshActionRenderer(ContextRequestViewAdapter):
    """Local user edit form 'refresh' action renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        folder = get_parent(self.context, IUsersFolderPlugin)
        return {
            'status': 'success',
            'message': self.request.localizer.translate(_("This profile has been deactivated!"
                                                          "<br /> "
                                                          "A new activation code has been "
                                                          "created and sent to this user!")),
            'callbacks': [
                get_json_table_row_refresh_callback(folder, self.request,
                                                    LocalUsersSearchResultsTable, self.context)
            ]
        }


@adapter_config(name='enable',
                required=(ILocalUser, IAdminLayer, LocalUserEditForm),
                provides=IAJAXFormRenderer)
class LocalUserEditFormEnableActionRenderer(ContextRequestViewAdapter):
    """Local user edit form 'enable' action renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        translate = self.request.localizer.translate
        folder = get_parent(self.context, IUsersFolderPlugin)
        return {
            'status': 'success',
            'messagebox': {
                'status': 'success',
                'timeout': 10000,
                'title': translate(_("Enabled user!")),
                'icon': 'fas fa-info-circle',
                'message': translate(_("User has been enabled and can now log-in!"))
            },
            'callbacks': [
                get_json_table_row_refresh_callback(folder, self.request,
                                                    LocalUsersSearchResultsTable, self.context)
            ]
        }


@adapter_config(name='disable',
                required=(ILocalUser, IAdminLayer, LocalUserEditForm),
                provides=IAJAXFormRenderer)
class LocalUserEditFormDisableActionRenderer(ContextRequestViewAdapter):
    """Local user edit form 'disable' action renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        translate = self.request.localizer.translate
        folder = get_parent(self.context, IUsersFolderPlugin)
        return {
            'status': 'success',
            'messagebox': {
                'status': 'warning',
                'timeout': 10000,
                'title': translate(_("Disabled user!")),
                'icon': 'fas fa-info-circle',
                'message': translate(_("User has been disabled and can't log in anymore!"))
            },
            'callbacks': [
                get_json_table_row_refresh_callback(folder, self.request,
                                                    LocalUsersSearchResultsTable, self.context)
            ]
        }


@adapter_config(required=(ILocalUser, IAdminLayer, Interface),
                provides=ITableElementEditor)
class LocalUserEditor(TableElementEditor):
    """Local user editor adapter"""


@adapter_config(required=ILocalUser, provides=IViewContextPermissionChecker)
class LocalUserPermissionChecker(ContextAdapter):
    """Local user permission checker"""

    edit_permission = MANAGE_SECURITY_PERMISSION


@ajax_form_config(name='change-password.html', context=ILocalUser, layer=IPyAMSLayer,
                  permission=MANAGE_SECURITY_PERMISSION)
class LocalUserPasswordChangeForm(InnerSecurityPluginFormMixin, AdminModalEditForm):
    """Local user password change form"""

    @property
    def title(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        return '{}<br /><small>{}</small>'.format(
            super().title,
            translate(_("User: {}")).format(self.context.title))

    legend = _("Change user password")

    fields = Fields(ILocalUser).select('password_manager', 'password', 'confirmed_password')


@subscriber(IDataExtractedEvent, form_selector=LocalUserPasswordChangeForm)
def extract_local_user_password_form_data(event):
    """Check new local user password data"""
    data = event.data
    password = data.get('password')
    if password and (password != data.get('confirmed_password')):
        event.form.widgets.errors += (Invalid(_("User password was not confirmed correctly.")),)
    else:
        del data['confirmed_password']
