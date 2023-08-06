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

"""PyAMS_zmi.zmi.skin module

Generic skin management components.
"""

from zope.interface import Interface, alsoProvides, implementer

from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IForm, IGroup, IInnerSubForm
from pyams_form.subform import InnerEditForm
from pyams_layer.interfaces import IPyAMSLayer, ISkinnable, IUserSkinnable, MANAGE_SKIN_PERMISSION
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, FormGroupChecker
from pyams_zmi.helper.event import get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_zmi import _


@viewlet_config(name='user-skin-properties.menu',
                context=IUserSkinnable, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=500,
                permission=MANAGE_SKIN_PERMISSION)
class UserSkinnablePropertiesMenuItem(NavigationMenuItem):
    """User skin properties menu"""

    label = _("Graphic theme")
    href = '#user-skin-properties.html'


class IUserSkinPropertiesForm(Interface):
    """User skin properties edit form marker interface"""


@ajax_form_config(name='user-skin-properties.html',
                  context=IUserSkinnable, layer=IPyAMSLayer,
                  permission=MANAGE_SKIN_PERMISSION)
class UserSkinPropertiesEditForm(AdminEditForm):
    """User skin properties edit form"""

    title = _("Graphic theme")

    def __init__(self, context, request):
        super().__init__(context, request)
        if not IUserSkinnable(context).can_inherit_skin:
            alsoProvides(self, IUserSkinPropertiesForm)


@adapter_config(name='skin-override',
                required=(IUserSkinnable, IAdminLayer, UserSkinPropertiesEditForm),
                provides=IGroup)
@implementer(IUserSkinPropertiesForm)
class UserSkinPropertiesInheritGroup(FormGroupChecker):
    """User skin properties inherit group"""

    def __new__(cls, context, request, parent_form):
        if not IUserSkinnable(context).can_inherit_skin:
            return None
        return FormGroupChecker.__new__(cls)

    fields = Fields(IUserSkinnable).select('override_skin')
    checker_fieldname = 'override_skin'
    checker_mode = 'disable'


@adapter_config(name='user-skin-properties',
                required=(IUserSkinnable, IAdminLayer, IUserSkinPropertiesForm),
                provides=IInnerSubForm)
class UserSkinPropertiesInnerEditForm(InnerEditForm):
    """User skin properties inner edit form"""

    @property
    def legend(self):
        if IUserSkinnable(self.context).can_inherit_skin:
            return None
        return _("Skin properties")

    border_class = ''

    fields = Fields(IUserSkinnable).select('skin', 'container_class', 'custom_stylesheet',
                                           'editor_stylesheet', 'custom_script')


@adapter_config(required=(IUserSkinnable, IAdminLayer, UserSkinPropertiesInnerEditForm),
                provides=IAJAXFormRenderer)
class UserSkinPropertiesInnerEditFormRenderer(ContextRequestViewAdapter):
    """User skin properties inner edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        callbacks = []
        if 'custom_stylesheet' in changes.get(ISkinnable, ()):
            callbacks.append(get_json_widget_refresh_callback(self.view, 'custom_stylesheet'))
        if 'editor_stylesheet' in changes.get(ISkinnable, ()):
            callbacks.append(get_json_widget_refresh_callback(self.view, 'editor_stylesheet'))
        if 'custom_script' in changes.get(ISkinnable, ()):
            callbacks.append(get_json_widget_refresh_callback(self.view, 'custom_script'))
        form = self.view.parent_form
        while not hasattr(form, 'success_message'):
            form = form.parent_form
        return {
            'status': 'success',
            'message': self.request.localizer.translate(form.success_message),
            'callbacks': callbacks
        }
