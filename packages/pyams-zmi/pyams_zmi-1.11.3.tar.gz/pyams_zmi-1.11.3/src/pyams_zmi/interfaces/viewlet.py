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

"""PyAMS_zmi.interfaces.viewlet module

This module defines public interfaces of several content providers which are used
in PyAMS management interface.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface
from zope.schema import Bool, Choice, TextLine

from pyams_skin.interfaces import BOOTSTRAP_STATUS
from pyams_skin.interfaces.viewlet import IDropdownMenu
from pyams_viewlet.interfaces import IViewletManager


class IPageHeaderViewletManager(IViewletManager):
    """Header viewlet marker interface"""


class ITopLinksViewletManager(IViewletManager):
    """Top links viewlet marker interface"""


class IUserLinksViewletManager(IViewletManager):
    """User links viewlet marker interface"""


class IUserMenuViewletManager(IViewletManager):
    """User menu viewlet marker interface"""


class ILeftAsideViewletManager(IViewletManager):
    """Left aside viewlet marker interface"""


class INavigationViewletManager(IViewletManager):
    """Navigation viewlet marker interface"""


class IMenuHeader(Interface):
    """Menu header"""


class INavigationMenu(IViewletManager):
    """Navigation menu viewlet interface"""

    header = TextLine(title="Menu header label",
                      description="Can be customized using an IMenuHeader multi-adapter")


class IContentManagementMenu(INavigationMenu):
    """Content management menu marker interface"""


class IPropertiesMenu(INavigationMenu):
    """Content properties menu"""


class ISiteManagementMenu(INavigationMenu):
    """Site management menu marker interface"""


class IControlPanelMenu(INavigationMenu):
    """Control panel menu marker interface"""


class IUtilitiesMenu(INavigationMenu):
    """Local utilities menu"""


class INavigationMenuItem(IViewletManager):
    """Navigation menu item viewlet interface"""

    label = TextLine(title="Main menu item label")

    css_class = TextLine(title="Main CSS class")

    icon_class = TextLine(title="FontAwesome class of menu item icon, including prefix "
                                "('fa', 'fab'...)")

    badge = TextLine(title="Optional badge text")

    badge_status = Choice(title="Badge status",
                          values=BOOTSTRAP_STATUS,
                          default='info')

    href = TextLine(title="Link target URL",
                    default='#')

    def get_href(self):
        """Complete HREF attribute getter"""

    click_handler = TextLine(title="Optional Javascript click handler name")

    target = TextLine(title="Menu link target name")

    modal_target = Bool(title="Link to modal dialog?",
                        default=False)


class IToolbarViewletManager(IViewletManager):
    """Toolbar viewlet manager"""


class IContextAddingsViewletManager(IDropdownMenu):
    """Context addings viewlet manager"""


class IActionsViewletManager(IViewletManager):
    """Custom actions menu viewlet manager"""
