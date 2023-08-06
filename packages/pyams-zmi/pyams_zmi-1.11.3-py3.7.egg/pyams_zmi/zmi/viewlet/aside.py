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

"""PyAMS_zmi.zmi.aside module

This module defines several content providers and viewlets which are used inside PyAMS
management interface navigation panel.
"""

from pyams_template.template import template_config
from pyams_viewlet.manager import TemplateBasedViewletManager, WeightOrderedViewletManager, \
    viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import ILeftAsideViewletManager


__docformat__ = 'restructuredtext'


@viewletmanager_config(name='pyams.page_aside', layer=IAdminLayer,
                       provides=ILeftAsideViewletManager)
@template_config(template='templates/page-aside.pt')
class LeftAsideViewletManager(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """Left aside viewlet manager"""


@viewlet_config(name='ajax-gear', layer=IAdminLayer,
                manager=ILeftAsideViewletManager, weight=1)
@template_config(template='templates/ajax-gear.pt')
class AJAXGearViewlet:
    """AJAX gear viewlet"""


@viewlet_config(name='version', layer=IAdminLayer,
                manager=ILeftAsideViewletManager, weight=999)
@template_config(template='templates/version.pt')
class VersionViewlet:
    """Version viewlet"""
