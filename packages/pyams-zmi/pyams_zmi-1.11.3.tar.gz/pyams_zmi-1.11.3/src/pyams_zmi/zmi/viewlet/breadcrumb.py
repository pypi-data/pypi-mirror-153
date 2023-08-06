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

"""PyAMS_zmi.zmi.viewlet.breadcrumb module

This module defines breadcrumbs adapter for management interface.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface
from zope.location import ILocation

from pyams_i18n.interfaces import II18n
from pyams_site.interfaces import ISiteRoot
from pyams_skin.interfaces.viewlet import IBreadcrumbItem
from pyams_skin.viewlet.breadcrumb import BreadcrumbItem
from pyams_utils.adapter import adapter_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.configuration import IZMIConfiguration


@adapter_config(required=(ILocation, IAdminLayer, Interface),
                provides=IBreadcrumbItem)
class AdminLayerBreadcrumbItem(BreadcrumbItem):
    """Admin layer breadcrumb ietm adapter"""

    view_name = 'admin'


@adapter_config(required=(ISiteRoot, IAdminLayer, Interface),
                provides=IBreadcrumbItem)
class SiteRootBreadcrumbItem(AdminLayerBreadcrumbItem):
    """Site root breadcrumb item adapter"""

    @property
    def label(self):
        """Label getter"""
        configuration = IZMIConfiguration(self.request.root)
        return II18n(configuration).query_attribute('home_name', request=self.request) or \
            configuration.site_name

    css_class = 'breadcrumb-item persistent'
