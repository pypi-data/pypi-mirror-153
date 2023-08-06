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

"""PyAMS_zmi.zmi.viewlet.nav module

This module is used to define components which are used to build navigation menu.
"""

from pyams_template.template import template_config
from pyams_viewlet.manager import TemplateBasedViewletManager, WeightOrderedViewletManager, \
    viewletmanager_config
from pyams_viewlet.viewlet import Viewlet, viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.configuration import IZMIConfiguration
from pyams_zmi.interfaces.viewlet import ILeftAsideViewletManager, INavigationViewletManager, \
    IUserLinksViewletManager


__docformat__ = 'restructuredtext'


@viewletmanager_config(name='pyams.page_nav', layer=IAdminLayer,
                       manager=ILeftAsideViewletManager, weight=50,
                       provides=INavigationViewletManager)
@template_config(template='templates/page-nav.pt')
class NavigationViewletManager(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """Navigation viewlet manager"""


@viewlet_config(name='hide-nav', layer=IAdminLayer,
                manager=IUserLinksViewletManager, weight=999)
@template_config(template='templates/hide-nav.pt')
class HideNavigationViewlet(Viewlet):
    """Hide navigation viewlet"""

    def __new__(cls, context, request, view, manager):  # pylint: disable=unused-argument
        configuration = IZMIConfiguration(request.root)
        if (configuration is None) or not configuration.include_minify_button:
            return None
        return Viewlet.__new__(cls)
