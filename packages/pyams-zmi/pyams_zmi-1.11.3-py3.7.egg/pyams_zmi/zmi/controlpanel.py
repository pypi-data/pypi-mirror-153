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

"""PyAMS_zmi.controlpanel module

This module defines views and content providers which are used to get access to the local
site manager contents view.
"""

from zope.interface import Interface, implementer
from zope.intid import IIntIds
from zope.principalannotation.interfaces import IPrincipalAnnotationUtility

from pyams_file.interfaces import IBlobReferenceManager
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.timezone import IServerTimezone
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.table import ITableWithActions
from pyams_zmi.interfaces.viewlet import IControlPanelMenu, IUtilitiesMenu
from pyams_zmi.table import NameColumn, Table, TableAdminView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_zmi import _  # pylint: disable=ungrouped-import


#
# Generic utilities labels
#

@adapter_config(required=(IBlobReferenceManager, IAdminLayer, Interface),
                provides=IObjectLabel)
def blob_reference_manager_label(context, request, view):
    """Blobs references manager label"""
    return request.localizer.translate(_("Blobs references manager"))


@adapter_config(required=(IIntIds, IAdminLayer, Interface),
                provides=IObjectLabel)
def intids_label(context, request, view):
    """Internal IDs label"""
    return request.localizer.translate(_("Internal IDs"))


@adapter_config(required=(IServerTimezone, IAdminLayer, Interface),
                provides=IObjectLabel)
def timezone_label(context, request, view):
    """Server timezone label getter"""
    return request.localizer.translate(_("Server timezone"))


@adapter_config(required=(IPrincipalAnnotationUtility, IAdminLayer, Interface),
                provides=IObjectLabel)
def principal_annotation_utility_label(context, request, view):
    """Principal annotation utility label getter"""
    return request.localizer.translate(_("Principals annotations"))


@viewletmanager_config(name='utilities.menu', context=ISiteRoot, layer=IAdminLayer,
                       manager=IControlPanelMenu, weight=10,
                       permission=VIEW_SYSTEM_PERMISSION, provides=IUtilitiesMenu)
class UtilitiesMenuItem(NavigationMenuItem):
    """Utilities menu item"""

    label = _("Utilities")
    icon_class = 'fab fa-codepen'
    href = '#utilities.html'


@implementer(ITableWithActions)
class UtilitiesTable(Table):
    """Utilities table list"""

    @property
    def data_attributes(self):
        attributes = super().data_attributes
        attributes.setdefault('table', {}).setdefault('data-page-length', 25)
        return attributes


@adapter_config(required=(ISiteRoot, IAdminLayer, UtilitiesTable),
                provides=IValues)
class UtilitiesTableValues(ContextRequestViewAdapter):
    """Utilities tables values adapter"""

    @property
    def values(self):
        """Utilities table values"""
        sm = self.context.getSiteManager()  # pylint: disable=invalid-name
        yield from sm.values()


@adapter_config(name='name',
                required=(ISiteRoot, IAdminLayer, UtilitiesTable),
                provides=IColumn)
class UtilityNameColumn(NameColumn):
    """Utility name column"""


@pagelet_config(name='utilities.html', context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class UtilitiesView(TableAdminView):
    """Utilities view"""

    title = _("Control panel")
    table_class = UtilitiesTable
    table_label = _("Site utilities")
