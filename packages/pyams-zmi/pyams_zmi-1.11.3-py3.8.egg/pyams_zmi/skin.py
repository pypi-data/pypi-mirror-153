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

"""PyAMS_zmi.skin module

This module defines PyAMS management skin layer.
"""

from pyams_layer.interfaces import ISkin
from pyams_utils.registry import utility_config
from pyams_zmi.interfaces import IAdminLayer, PYAMS_ADMIN_SKIN_NAME


__docformat__ = 'restructuredtext'

from pyams_zmi import _


@utility_config(name=PYAMS_ADMIN_SKIN_NAME, provides=ISkin)
class AdminSkin:
    """PyAMS administration skin"""

    label = _("PyAMS management skin")
    layer = IAdminLayer
