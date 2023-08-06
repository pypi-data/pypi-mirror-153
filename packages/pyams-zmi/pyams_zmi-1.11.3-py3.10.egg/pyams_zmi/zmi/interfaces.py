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

"""PyAMS_zmi.interfaces module

This module provides configuration menu interfaces.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_zmi.interfaces.viewlet import INavigationMenuItem


class IConfigurationMenu(INavigationMenuItem):
    """Configuration menu"""


class IUserProfileEditForm(Interface):
    """Marker interface for user profile edit form"""
