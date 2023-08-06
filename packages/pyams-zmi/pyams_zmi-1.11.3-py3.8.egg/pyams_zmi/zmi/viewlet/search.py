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

"""PyAMS_zmi.zmi.viewlet.search module

This module provides "pyams.site_search" viewlet, which is used to display a global site
search entry in PyAMS management interface.
"""

from pyams_template.template import template_config
from pyams_viewlet.viewlet import Viewlet, viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.configuration import IZMIConfiguration
from pyams_zmi.interfaces.viewlet import IUserLinksViewletManager


__docformat__ = 'restructuredtext'


@viewlet_config(name='pyams.site_search', layer=IAdminLayer,
                manager=IUserLinksViewletManager, weight=50)
@template_config(template='templates/site-search.pt')
class UserSearchViewlet(Viewlet):
    """User search viewlet"""

    def __new__(cls, context, request, view, manager):  # pylint: disable=unused-argument
        configuration = IZMIConfiguration(request.root, None)
        if (configuration is None) or not configuration.include_site_search:
            return None
        return Viewlet.__new__(cls)
