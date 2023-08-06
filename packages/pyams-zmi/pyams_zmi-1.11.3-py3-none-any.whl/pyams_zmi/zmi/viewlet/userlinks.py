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

"""PyAMS_zmi.zmi.viewlet.userlinks module

This module provides "pyams.userlinks" viewlet manager as well as other components which are
used to add links on top of PyAMS management interface.
"""

from pyams_security.interfaces.names import UNKNOWN_PRINCIPAL_ID
from pyams_skin.viewlet.menu import MenuDivider, MenuItem
from pyams_template.template import template_config
from pyams_viewlet.manager import TemplateBasedViewletManager, WeightOrderedViewletManager, \
    viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.profile import IUserProfile
from pyams_zmi.interfaces.viewlet import IPageHeaderViewletManager, IUserLinksViewletManager, \
    IUserMenuViewletManager


__docformat__ = 'restructuredtext'

from pyams_zmi import _  # pylint: disable=ungrouped-imports


@viewletmanager_config(name='pyams.userlinks', layer=IAdminLayer,
                       manager=IPageHeaderViewletManager, weight=900,
                       provides=IUserLinksViewletManager)
@template_config(template='templates/user-links.pt')
class UserLinksViewletManager(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """User links viewlet manager"""


@viewletmanager_config(name='pyams.usermenu', layer=IAdminLayer,
                       manager=IUserLinksViewletManager, weight=900,
                       provides=IUserMenuViewletManager)
@template_config(template='templates/user-menu.pt')
class UserMenuViewletManager(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """User menu viewlet manager"""

    def __new__(cls, context, request, view, manager=None):  # pylint: disable=unused-argument
        principal = request.principal
        if principal.id == UNKNOWN_PRINCIPAL_ID:
            return None
        return WeightOrderedViewletManager.__new__(cls)

    @property
    def profile_icon(self):
        """Profile icon getter"""
        result = None
        profile = IUserProfile(self.request, None)
        if profile is not None:
            result = profile.get_avatar()
        return result or '/--static--/myams/img/profile.png'


@viewlet_config(name='username.menu', layer=IAdminLayer,
                manager=IUserMenuViewletManager, weight=1)
class UserNameMenuItem(MenuItem):
    """Logged in user name menu"""

    href = 'user-profile.html'
    modal_target = True

    css_class = 'bg-primary text-white'
    icon_class = 'fa fa-user-circle'

    @property
    def label(self):
        """Label getter"""
        return '<strong>{}</strong>'.format(self.request.principal.title)


@viewlet_config(name='logout.divider', layer=IAdminLayer,
                manager=IUserMenuViewletManager, weight=999)
class LogoutMenuDivider(MenuDivider):
    """Logout menu divider"""


@viewlet_config(name='logout.menu', layer=IAdminLayer,
                manager=IUserMenuViewletManager, weight=1000)
class LogoutMenuItem(MenuItem):
    """Logout menu item"""

    icon_class = 'fa fa-sign-out-alt'
    label = _("Logout")
    href = 'logout'
