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

"""PyAMS_zmi.zmi.viewlet.logo module

"pyams.logo" is a viewlet which is used to display a logo in PyAMS top panel.
This logo is extracted from ZMI configuration.
"""

__docformat__ = 'restructuredtext'

from pyams_template.template import template_config
from pyams_viewlet.viewlet import Viewlet, viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.configuration import IZMIConfiguration
from pyams_zmi.interfaces.viewlet import IPageHeaderViewletManager


@viewlet_config(name='pyams.logo', layer=IAdminLayer,
                manager=IPageHeaderViewletManager, weight=0)
@template_config(template='templates/logo.pt')
class LogoViewlet(Viewlet):
    """Logo viewlet"""

    href = '/admin'

    @property
    def logo(self):
        """Logo getter"""
        configuration = IZMIConfiguration(self.request.root, None)
        if not configuration:
            return None
        return configuration.logo
