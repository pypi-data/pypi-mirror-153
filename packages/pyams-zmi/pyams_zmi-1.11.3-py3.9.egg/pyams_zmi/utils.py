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

"""PyAMS_zmi.utils module

This module provides a small set of generic components.
"""

from zope.component import queryAdapter, queryMultiAdapter
from zope.location import ILocation

from pyams_utils.adapter import adapter_config
from pyams_zmi.interfaces import IObjectHint, IObjectIcon, IObjectLabel


__docformat__ = 'restructuredtext'


@adapter_config(required=ILocation, provides=IObjectLabel)
def location_label(context):
    """Basic location name factory"""
    return context.__name__


def get_object_label(context, request, view=None):
    """Get object label"""
    adapter = queryMultiAdapter((context, request, view), IObjectLabel)
    if adapter is None:
        adapter = queryAdapter(context, IObjectLabel)
    return adapter


@adapter_config(required=ILocation, provides=IObjectIcon)
def location_icon(context):  # pylint: disable=unused-argument
    """Basic location icon factory"""
    return 'far fa-square'


def get_object_icon(context, request, view=None):
    """Get object icon"""
    adapter = queryMultiAdapter((context, request, view), IObjectIcon)
    if adapter is None:
        adapter = queryAdapter(context, IObjectIcon)
    return adapter


def get_object_hint(context, request, view=None):
    """Get object hint"""
    adapter = queryMultiAdapter((context, request, view), IObjectHint)
    if adapter is None:
        adapter = queryAdapter(context, IObjectHint)
    return adapter
