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

"""PyAMS_zmi.zmi.profile module

This module provides components used for user profile management.
"""

from zope.interface import Interface, implementer

from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_zmi.form import AdminModalEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.configuration import IZMIConfiguration
from pyams_zmi.interfaces.profile import IUserProfile
from pyams_zmi.zmi.interfaces import IUserProfileEditForm


__docformat__ = 'restructuredtext'

from pyams_zmi import _


@ajax_form_config(name='user-profile.html',
                  layer=IPyAMSLayer)
@implementer(IUserProfileEditForm)
class UserProfileEditForm(AdminModalEditForm):
    """User profile edit form"""

    legend = _("User profile")
    modal_class = 'modal-xl'

    @property
    def fields(self):
        fields = Fields(IUserProfile)
        if not IZMIConfiguration(self.request.root).user_bundle_selection:
            fields = fields.omit('zmi_bundle')
        return fields

    def get_content(self):
        return IUserProfile(self.request.principal)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        bundle = self.widgets.get('zmi_bundle')
        if bundle is not None:
            bundle.no_value_message = _("Use default theme")


@adapter_config(required=(Interface, IAdminLayer, IUserProfileEditForm),
                provides=IAJAXFormRenderer)
class UserProfileEditFormRenderer(AJAXFormRenderer):
    """User profile edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes:
            return {
                'status': 'redirect'
            }
        return super().render(changes)
