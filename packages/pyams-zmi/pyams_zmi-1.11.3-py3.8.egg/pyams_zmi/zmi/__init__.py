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

"""PyAMS_zmi.zmi module

This module defines the global management interface view!
"""

from zope.interface import Interface

from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_template.template import template_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.view import AdminView


__docformat__ = 'restructuredtext'


@pagelet_config(name='admin', context=Interface, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
@template_config(template='templates/admin-index.pt',
                 layer=IAdminLayer)
class AdminPage(AdminView):
    """Main management page"""
