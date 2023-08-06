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

"""PyAMS_zmi.interfaces.table module

This module defines public interfaces of table views.
"""

from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, TextLine

from pyams_template.template import template_config
from pyams_zmi.interfaces import IInnerAdminView


__docformat__ = 'restructuredtext'

from pyams_zmi import _


@template_config(template='templates/table.pt')
@template_config(template='templates/table-empty.pt', name='empty')
class ITableView(Interface):
    """Table view interface"""


class ITableAdminView(ITableView, IInnerAdminView):
    """Admin table view interface"""

    table_class = Attribute("Inner table class")

    table_label = TextLine(title="Inner table label")


@template_config(template='templates/inner-table.pt')
@template_config(template='templates/inner-table-empty.pt', name='empty')
class IInnerTable(IContentProvider):
    """Inner admin table view interface"""

    table_class = Attribute("Inner table class")

    table_label = TextLine(title="Inner table label")


@template_config(template='templates/table-multiple.pt')
class IMultipleTableView(IInnerAdminView):
    """Multiple table view"""


class ITableWithActions(Interface):
    """Marker interface for table with inner actions menu"""


@template_config(template='templates/table-switcher.pt')
class ITableGroupSwitcher(Interface):
    """Table group switcher interface"""

    legend = TextLine(title=_("Switcher legend"),
                      required=True)

    minus_class = TextLine(title="Expanded switcher FontAwesome CSS class (without prefix)",
                           default='minus')

    plus_class = TextLine(title="Reduced switcher FontAwesome CSS class (without prefix)",
                          default='plus')

    switcher_mode = Choice(title="Switcher display mode",
                           values=('always', 'never', 'auto'),
                           default='auto')

    state = Attribute("Initial switcher state")


class ITableElementEditor(Interface):
    """Table row element editor marker interface"""

    view_name = TextLine(title="Editor view name",
                         default='properties.html')

    href = TextLine(title="Editor URL")

    modal_target = Bool(title="Modal target?",
                        required=True,
                        default=True)


class IReorderColumn(Interface):
    """Reorder column marker interface"""
