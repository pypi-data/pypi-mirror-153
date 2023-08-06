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

"""PyAMS_zmi.zmi.viewlet.ribbon module

This modules defines "pyams.page_ribbon", which is used to build PyAMS breadcrumbs ribbon of
the management interface.
"""

from pyams_template.template import template_config
from pyams_viewlet.viewlet import ViewContentProvider, contentprovider_config
from pyams_zmi.interfaces import IAdminLayer


__docformat__ = 'restructuredtext'


@contentprovider_config(name='pyams.page_ribbon', layer=IAdminLayer)
@template_config(template='templates/page-ribbon.pt')
class RibbonContentProvider(ViewContentProvider):
    """Ribbon content provider"""
