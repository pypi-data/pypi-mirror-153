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

"""PyAMS_zmi.registry module

This module defines components which are used to display local and global registries contents.
"""

from html import escape

from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import MANAGE_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_skin.interfaces.viewlet import IHelpViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_local_registry, get_pyramid_registry
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.viewlet import IUtilitiesMenu
from pyams_zmi.table import NameColumn, Table, TableAdminView
from pyams_zmi.utils import get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_zmi import _


class RegistryTable(Table):
    """Base registry table"""


@adapter_config(name='component',
                required=(ISiteRoot, IAdminLayer, RegistryTable),
                provides=IColumn)
class RegistryTableComponentColumn(NameColumn):
    """Registry table component column"""

    i18n_header = _("Component")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 10

    def get_value(self, obj):
        """Component column value getter"""
        component = obj.component
        if component is not None:
            name = get_object_label(component, request=self.request, view=self.table)
            if not name:
                name = getattr(component, '__name__', None)
            if not name:
                name = str(component.__class__)
        else:
            name = str(obj.factory)
        return escape(name)


@adapter_config(name='interface',
                required=(ISiteRoot, IAdminLayer, RegistryTable),
                provides=IColumn)
class RegistryTableInterfaceColumn(NameColumn):
    """Registry table interface column"""

    i18n_header = _("Interface")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 20

    def get_value(self, obj):
        """Interface column value getter"""
        return escape(str(obj.provided))


@adapter_config(name='name',
                required=(ISiteRoot, IAdminLayer, RegistryTable),
                provides=IColumn)
class RegistryTableNameColumn(NameColumn):
    """Registry table name column"""

    i18n_header = _("Name")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 30

    def get_value(self, obj):
        """Name column value getter"""
        return obj.name or '--'


#
# Local registry views
#

@viewlet_config(name='local-registry.menu', context=ISiteRoot, layer=IAdminLayer,
                manager=IUtilitiesMenu, weight=10,
                permission=MANAGE_SYSTEM_PERMISSION)
class LocalRegistryMenu(NavigationMenuItem):
    """Local registry menu"""

    label = _("Local registry")
    href = '#local-registry.html'


class LocalRegistryTable(RegistryTable):
    """Local registry table"""


@adapter_config(required=(ISiteRoot, IAdminLayer, LocalRegistryTable),
                provides=IValues)
class LocalRegistryTableValues(ContextRequestViewAdapter):
    """Local registry table values adapter"""

    @property
    def values(self):
        """Local registry table values getter"""
        yield from get_local_registry().registeredUtilities()


@pagelet_config(name='local-registry.html', context=ISiteRoot, layer=IPyAMSLayer,
                permission=MANAGE_SYSTEM_PERMISSION)
class LocalRegistryView(TableAdminView):
    """Local registry view"""

    title = _("Site utilities")
    table_class = LocalRegistryTable
    table_label = _("Local registry")


@viewlet_config(name='local-registry.info', context=ISiteRoot, layer=IAdminLayer,
                view=LocalRegistryView, manager=IHelpViewletManager, weight=1)
class LocalRegistryInfo(AlertMessage):
    """Local registry info"""

    status = 'info'
    css_class = 'mx-2'
    _message = _("""The local registry is used to store 'local' utilities, whose configuration \
is stored into the ZODB. Some of these utilities have important settings which can define \
the whole application behaviour.\n
Some of these components are created automatically, while other ones are created by sites \
managers, like SQLAlchemy or ZODB connections.
""")
    message_renderer = 'markdown'


#
# Global registry views
#

@viewlet_config(name='global-registry.menu', context=ISiteRoot, layer=IAdminLayer,
                manager=IUtilitiesMenu, weight=20,
                permission=MANAGE_SYSTEM_PERMISSION)
class GlobalRegistryMenu(NavigationMenuItem):
    """Global registry menu"""

    label = _("Global registry")
    href = '#global-registry.html'


class GlobalRegistryTable(RegistryTable):
    """Global registry table"""


@adapter_config(required=(ISiteRoot, IAdminLayer, GlobalRegistryTable),
                provides=IValues)
class GlobalRegistryTableValues(ContextRequestViewAdapter):
    """Global registry table values adapter"""

    @property
    def values(self):
        """Global registry table values getter"""
        yield from get_pyramid_registry().registeredUtilities()


@pagelet_config(name='global-registry.html', context=ISiteRoot, layer=IPyAMSLayer,
                permission=MANAGE_SYSTEM_PERMISSION)
class GlobalRegistryView(TableAdminView):
    """Global registry view"""

    title = _("Site utilities")
    table_class = GlobalRegistryTable
    table_label = _("Global registry")


@viewlet_config(name='global-registry.info', context=ISiteRoot, layer=IAdminLayer,
                view=GlobalRegistryView, manager=IHelpViewletManager, weight=1)
class GlobalRegistryInfo(AlertMessage):
    """Global registry info"""

    status = 'info'
    css_class = 'mx-2'
    _message = _("""The global registry is used to store utilities which are defined statically \
in Python code or using ZCML directives.
""")
