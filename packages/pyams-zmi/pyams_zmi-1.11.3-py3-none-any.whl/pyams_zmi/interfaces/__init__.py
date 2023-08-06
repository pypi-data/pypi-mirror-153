#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_zmi.interfaces module

Public interfaces module.
"""

from zope.interface import Interface
from zope.schema import TextLine

from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.interfaces.view import IFullPage, IInnerPage
from pyams_template.template import layout_config
from pyams_viewlet.interfaces import IViewletManager


class IAdminLayer(IPyAMSLayer):
    """PyAMS management layer"""


PYAMS_ADMIN_SKIN_NAME = 'PyAMS admin skin'


@layout_config(template='templates/admin-layout.pt')
class IAdminView(IFullPage):
    """Management view marker interface"""

    header_label = TextLine(title="Header label")


class IInnerAdminView(IInnerPage, IAdminView):
    """Inner management view marker interface"""

    title = TextLine(title="View title")


class ICompositeView(IViewletManager):
    """Composite view marker interface"""


class IPageTitle(Interface):
    """Simple page title interface"""


class IObjectLabel(Interface):
    """Object label getter interface"""


class IObjectIcon(Interface):
    """Object icon getter interface"""


class IObjectHint(Interface):
    """Object hint getter interface"""
