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

"""PyAMS_zmi.zmi.viewlet.toplinks module

This module provides "pyams.toplinks" viewlet manager and a small set of components which are
used to display tabs and links in PyAMS management interface.
"""

from pyams_template.template import template_config
from pyams_utils.data import ObjectDataManagerMixin
from pyams_viewlet.manager import TemplateBasedViewletManager, WeightOrderedViewletManager,\
    viewletmanager_config
from pyams_viewlet.viewlet import Viewlet
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPageHeaderViewletManager, ITopLinksViewletManager


__docformat__ = 'restructuredtext'


@viewletmanager_config(name='pyams.toplinks', layer=IAdminLayer,
                       manager=IPageHeaderViewletManager, weight=100,
                       provides=ITopLinksViewletManager)
@template_config(template='templates/top-links.pt')
class TopLinksViewletManager(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """Top links viewlet manager"""


@template_config(template='templates/top-menu.pt')
class TopMenuViewletManager(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """Top menu viewlet manager"""

    min_display_size = ''
    """Minimum media display size; can be 'sm', 'md'..."""

    label = 'Menu label'
    """Menu label"""

    selection = '(selected value)'
    """Displayed menu selection"""


@template_config(template='templates/top-menus-group.pt')
class TopMenusGroupViewletManager(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """Top menus group viewlet manager"""

    min_display_size = ''
    """Minimum media display size; can be 'sm', 'md'..."""

    label = 'Group label'
    """Menus group label"""


@template_config(template='templates/top-menu-item.pt')
class TopMenuItem(ObjectDataManagerMixin, Viewlet):
    """Top menu item"""

    label = 'Menu item label'
    """Menu item label"""

    href = '/'
    """Menu URL target"""

    css_class = 'dropdown-item'
    """CSS class"""


@template_config(template='templates/top-tabs.pt')
class TopTabsViewletManager(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """Top tabs viewlet manager"""

    min_display_size = ''
    """Minimum media display size; can be 'sm', 'md'..."""

    label = 'Tabs label'
    """Tabs group label"""


@template_config(template='templates/top-tab.pt')
class TopTabItem(ObjectDataManagerMixin, Viewlet):
    """Top tab item base class"""

    label = 'Tab item label'
    """Tab item label"""

    href = '#content'
    """Tab content target"""

    url = '/admin'
    """URL pointed by the tab"""
