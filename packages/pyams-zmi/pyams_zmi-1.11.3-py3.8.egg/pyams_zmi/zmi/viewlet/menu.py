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

"""PyAMS_zmi.viewlet.menu module

This module provides components and content providers which are used to build PyAMS
navigation menu.
"""

from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_template.template import template_config
from pyams_utils.data import ObjectDataManagerMixin
from pyams_viewlet.manager import TemplateBasedViewletManager, WeightOrderedViewletManager, \
    viewletmanager_config
from pyams_viewlet.viewlet import Viewlet
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IControlPanelMenu, IMenuHeader, \
    INavigationMenu, INavigationMenuItem, INavigationViewletManager, ISiteManagementMenu


__docformat__ = 'restructuredtext'

from pyams_zmi import _


@template_config(template='templates/nav-menu.pt')
@implementer(INavigationMenu)
class NavigationMenu(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """Navigation menu"""

    _header = FieldProperty(INavigationMenu['header'])

    @property
    def header(self):
        """Menu header getter"""
        header = queryMultiAdapter((self.context, self.request, self.view, self), IMenuHeader)
        return header or self._header


@template_config(template='templates/nav-item.pt')
@implementer(INavigationMenuItem)
class NavigationMenuItem(ObjectDataManagerMixin, TemplateBasedViewletManager,
                         WeightOrderedViewletManager):
    """Navigation menu item"""

    @property
    def render_empty(self):
        """Getter to check if empty menu should be rendered"""
        return bool(self.href or self.click_handler)

    css_class = FieldProperty(INavigationMenuItem['css_class'])
    icon_class = FieldProperty(INavigationMenuItem['icon_class'])
    label = FieldProperty(INavigationMenuItem['label'])
    badge = FieldProperty(INavigationMenuItem['badge'])
    badge_status = FieldProperty(INavigationMenuItem['badge_status'])
    href = FieldProperty(INavigationMenuItem['href'])
    click_handler = FieldProperty(INavigationMenuItem['click_handler'])
    target = FieldProperty(INavigationMenuItem['target'])
    modal_target = FieldProperty(INavigationMenuItem['modal_target'])

    def get_href(self):
        """Menu item URL getter"""
        return self.href


@template_config(template='templates/nav-header.pt')
class NavigationMenuHeaderDivider(Viewlet):
    """Navigation menu internal header"""


@template_config(template='templates/nav-divider.pt')
class NavigationMenuDivider(Viewlet):
    """Navigation menu divider"""


@viewletmanager_config(name='content-manager.menu', layer=IAdminLayer,
                       manager=INavigationViewletManager, weight=100,
                       provides=IContentManagementMenu)
class ContentManagementMenu(NavigationMenu):
    """Content management menu"""

    _header = _("Content management")


@viewletmanager_config(name='site-manager.menu', layer=IAdminLayer,
                       manager=INavigationViewletManager, weight=200,
                       provides=ISiteManagementMenu)
class SiteManagementMenu(NavigationMenu):
    """Site management menu"""

    _header = _("Site management")


@viewletmanager_config(name='control-panel.menu', layer=IAdminLayer,
                       manager=INavigationViewletManager, weight=300,
                       provides=IControlPanelMenu)
class ControlPanelMenu(NavigationMenu):
    """Control panel menu"""

    _header = _("Control panel")
