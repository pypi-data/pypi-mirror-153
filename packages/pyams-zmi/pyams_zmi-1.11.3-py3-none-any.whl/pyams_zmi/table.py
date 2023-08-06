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

"""PyAMS_zmi.table module

This module provides bases classes for tables management.
"""

import json
from pyramid.decorator import reify
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_security.interfaces import ISecurityContext
from pyams_security.permission import get_edit_permission, get_permission_checker
from pyams_security.security import ProtectedViewObjectMixin
from pyams_table.column import Column, GetAttrColumn
from pyams_table.table import Table as BaseTable, get_weight
from pyams_template.template import get_view_template
from pyams_utils.adapter import ContextRequestViewAdapter
from pyams_utils.data import ObjectDataManagerMixin
from pyams_utils.date import SH_DATE_FORMAT, format_datetime
from pyams_utils.factory import get_object_factory
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.list import boolean_iter
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import ViewContentProvider
from pyams_zmi.interfaces.table import IInnerTable, IMultipleTableView, IReorderColumn, \
    ITableAdminView, ITableElementEditor, ITableGroupSwitcher, ITableView
from pyams_zmi.utils import get_object_hint, get_object_icon, get_object_label
from pyams_zmi.view import InnerAdminView


__docformat__ = 'restructuredtext'

from pyams_zmi import _  # pylint: disable=ungrouped-imports


def get_table_id(table, context=None):
    """Table ID getter"""
    if context is None:
        context = table.context
    return f'{table.prefix}_{ICacheKeyValue(context)}'


def get_column_sort(column, ignored=None):  # pylint: disable=unused-argument
    """Get column sortable attribute"""
    return getattr(column, 'sortable', None)


def get_column_type(column, ignored=None):  # pylint: disable=unused-argument
    """Get column sort type attribute"""
    return getattr(column, 'sort_type', None)


def get_row_id(table, element, context=None):
    """Row ID getter"""
    return f'{table.id}::{ICacheKeyValue(element)}'


def get_row_name(element):
    """Row name getter"""
    return getattr(element, '__name__', None)


def get_row_editor(table, element):
    """Row editor getter"""
    return queryMultiAdapter((element, table.request, table), ITableElementEditor)


def check_attribute(attribute, source, column=None):
    """Check attribute value"""
    if callable(attribute):
        return attribute(source, column)
    return str(attribute)


def get_attributes(table, element, source, column=None):
    """Get table data attributes"""
    result = ''
    attrs = getattr(table, 'data_attributes', {}).get(element, {})
    for key, value in attrs.items():
        checked_value = check_attribute(value, source, column)
        if checked_value is not None:
            result += f" {key}='{checked_value}'"
    return result


def get_data_attributes(element):
    """Get object data attributes"""
    data = IObjectData(element, None)
    if data and data.object_data:
        return ' '.join((
            f"data-{k}='{v if isinstance(v, str) else json.dumps(v)}'"
            for k, v in data.object_data.items()
        ))
    return ''


def get_ordered_data_attributes(source, container, request, target='reorder.json'):
    """Get object data attributes for ordered table"""
    source.setdefault('table', {}).update({
        'data-searching': 'false',
        'data-info': 'false',
        'data-paging': 'false',
        'data-ams-order': '0,asc'
    })
    context = ISecurityContext(container, None)
    if context is None:
        context = request.context
    permission = get_edit_permission(request, context)
    if (not permission) or request.has_permission(permission, context=container):
        source.setdefault('table', {}).update({
            'data-ams-location': absolute_url(container, request),
            'data-row-reorder': '{"update": false}',
            'data-ams-reorder-url': target
        })
        source.setdefault('tr', {}).update({
            'data-ams-row-value': lambda row, col: get_row_name(row)
        })
        source.setdefault('td', {}).update({
            'data-order': lambda x, col: list(container.keys()).index(x.__name__)
                if IReorderColumn.providedBy(col) else None
        })


class Table(ObjectDataManagerMixin, BaseTable):
    """Extended table class"""

    @reify
    def id(self):  # pylint: disable=invalid-name
        """Table ID getter"""
        return get_table_id(self, self.context)

    batch_size = 500
    start_batching_at = 500

    css_classes = {
        'table': 'table table-striped table-hover table-sm datatable'
    }

    object_data = {
        'responsive': True,
        'auto-width': False
    }

    @property
    def data_attributes(self):
        """Table data attributes getter

        These attributes are to be use with DataTables plug-in, and can be overridden in
        subclasses.
        """
        return {
            'table': {
                'id': self.id,
                'data-ams-location': absolute_url(self.context, self.request)
            },
            'tr': {
                'id': lambda row, col: self.get_row_id(row),
                'data-ams-element-name': lambda row, col: get_row_name(row),
                'data-ams-url': lambda row, col: getattr(get_row_editor(self, row), 'href', None),
                'data-toggle':
                    lambda row, col: 'modal' if getattr(get_row_editor(self, row),
                                                        'modal_target', None)
                    else None
            },
            'th': {
                'data-ams-column-name': lambda row, col: row.__name__,
                'data-ams-sortable': get_column_sort,
                'data-ams-type': get_column_type
            }
        }

    def get_row_id(self, row):
        """Row ID getter"""
        return get_row_id(self, row)

    def get_selected_row_class(self, row, css_class=None):
        """Get selected row class"""
        klass = self.css_classes.get('tr.selected')
        if callable(klass):
            klass = klass(*row)
        return f"{css_class if css_class else ''} {klass if klass else ''}".strip()

    def render_table(self):
        return super().render_table() \
            .replace('<table', f"<table {get_attributes(self, 'table', self)}") \
            .replace('<table', f"<table {get_data_attributes(self)}")

    def render_row(self, row, css_class=None):
        css_class = self.get_selected_row_class(row[0], css_class)
        return super().render_row(row, css_class) \
            .replace('<tr', f"<tr {get_attributes(self, 'tr', row[0][0])}")

    def render_head_cell(self, column):
        return super().render_head_cell(column) \
            .replace('<th', f"<th {get_attributes(self, 'th', column)}") \
            .replace('<th', f"<th {get_data_attributes(column)}")

    def render_cell(self, item, column, colspan=0):
        return super().render_cell(item, column, colspan) \
            .replace('<td', f"<td {self.get_css_class('td', None, item, column)}") \
            .replace('<td', f"<td {get_attributes(self, 'td', item, column)}")


class InnerTableMixin:
    """Inner table mixin class"""

    table_class = Table
    table_label = FieldProperty(ITableAdminView['table_label'])

    container_intf = None
    container_name = ''

    empty_template = get_view_template(name='empty')

    def __init__(self, context, request, *args, **kwargs):
        super().__init__(context, request, *args, **kwargs)
        container = self.get_container()
        self.table = self.get_table(container)

    def get_container(self):
        """Table container getter"""
        if self.container_intf is None:
            return self.context
        registry = self.request.registry
        return registry.queryAdapter(self.context, self.container_intf,
                                     name=self.container_name)

    def get_table(self, container):
        """Table factory"""
        factory = get_object_factory(self.table_class)
        return factory(container, self.request)

    def update(self):
        """Admin view updater"""
        super().update()  # pylint: disable=no-member
        self.table.update()

    def render(self):
        """Admin view renderer"""
        has_values, values = boolean_iter(self.table.values)  # pylint: disable=no-member,unused-variable
        if (not has_values) and not getattr(self.table, 'display_if_empty', False):
            return self.empty_template()
        return super().render()  # pylint: disable=no-member


@implementer(ITableView)
class TableView(InnerTableMixin):
    """Table view

    This class is a wrapper for a base view including a table.
    """


@implementer(ITableAdminView)
class TableAdminView(InnerTableMixin, InnerAdminView):
    """Table admin view

    This class is a wrapper for an admin view based on an inner table.
    """


@implementer(IInnerTable)
class InnerTableAdminView(InnerTableMixin):
    """Inner table admin view"""


class MultipleTablesMixin:
    """Multiple tables mixin view class"""

    table_label = FieldProperty(ITableAdminView['table_label'])

    @reify
    def tables(self):
        """Tables getter"""
        registry = self.request.registry
        return sorted((
            table
            for name, table in registry.getAdapters((self.context, self.request, self),  # pylint: disable=no-member
                                                    IInnerTable)
        ), key=get_weight)

    def update(self):
        """View update"""
        super().update()
        for table in self.tables:
            table.update()


@implementer(IMultipleTableView)
class MultipleTablesAdminView(MultipleTablesMixin, InnerAdminView):
    """Multiple tables admin view"""


@implementer(ITableGroupSwitcher)
class TableGroupSwitcher(ObjectDataManagerMixin, InnerTableAdminView, ViewContentProvider):
    """Table group switcher

    This switcher group is very similar to the form group switcher, but is only
    used to handle an inner table.
    """

    legend = FieldProperty(ITableGroupSwitcher['legend'])
    minus_class = FieldProperty(ITableGroupSwitcher['minus_class'])
    plus_class = FieldProperty(ITableGroupSwitcher['plus_class'])
    switcher_mode = FieldProperty(ITableGroupSwitcher['switcher_mode'])

    @property
    def state(self):
        """Current state getter"""
        if self.switcher_mode == 'always':
            return 'open'
        if self.switcher_mode == 'never':
            return 'closed'
        # else: automatic mode
        has_values, _values = boolean_iter(self.table.values)
        return 'open' if has_values else 'closed'

    def get_forms(self, include_self=True):
        """Forms getter

        This method doesn't return anything, but  is used when component is used as
        an inner form adapter!
        """
        yield from ()


class I18nColumnMixin:
    """Column mixin with I18n header"""

    i18n_header = None

    @property
    def header(self):
        """Column header getter translation"""
        return self.request.localizer.translate(self.i18n_header)


@implementer(IReorderColumn)
class ReorderColumn(ProtectedViewObjectMixin, Column):
    """Reorder column"""

    weight = 0
    sortable = 'false'

    @property
    def css_classes(self):
        has_permission = self.has_permission(self.context)
        return {
            'th': f"{'reorder ' if has_permission else ''}action",
            'td': f"{'sorter mouse-move ' if has_permission else ''}action"
        }

    def has_permission(self, item):
        """Column permission test"""
        if not self.permission:
            return True
        return self.request.has_permission(self.permission, context=item)

    def render_cell(self, item):
        if not self.has_permission(item):
            return ''
        return '<i class="fas fa-arrows-alt-v"></i>'


class ContentTypeColumn(Column):
    """Content type column"""

    header = ''
    css_classes = {
        'th': 'action',
        'td': 'sorter text-center'
    }
    sortable = 'false'
    weight = 9

    def render_cell(self, item):
        icon = get_object_icon(item, self.request, self.table)
        if not icon:
            return ''
        hint = get_object_hint(item, self.request, self.table) or ''
        return f'<i class="{icon} hint" data-original-title="{hint}"></i>'


class NameColumn(I18nColumnMixin, GetAttrColumn):
    """Common name column"""

    i18n_header = _("Name")
    weight = 10

    def get_value(self, obj):
        return get_object_label(obj, self.request, self.table)


class IconColumn(Column):
    """Base icon column"""

    header = ''
    css_classes = {
        'th': 'action'
    }
    sortable = 'false'

    icon_class = ''
    hint = ''

    permission = None
    checker = None

    def render_cell(self, item):
        """Column cell renderer based on permission and checker"""
        if not self.has_permission(item):
            return ''
        if self.checker:
            if callable(self.checker):
                checked = self.checker(item)  # pylint: disable=not-callable
            else:
                checked = self.checker
            if not checked:
                return ''
        return self.get_icon(item)

    def has_permission(self, item):
        """Column permission test"""
        if not self.permission:
            return True
        return self.request.has_permission(self.permission, context=item)

    def get_icon(self, item):
        """Column icon getter"""
        hint = self.get_icon_hint(item)
        return f'''<i class="fa-fw {self.get_icon_class(item)} {'hint' if hint else ''}"''' \
               f''' data-original-title="{hint}"></i>'''

    def get_icon_class(self, item):  # pylint: disable=unused-argument
        """Column class getter"""
        return self.icon_class

    def get_icon_hint(self, item):  # pylint: disable=unused-argument
        """Column hint getter"""
        return self.request.localizer.translate(self.hint)


class BaseActionColumn(IconColumn):
    """Base action column"""

    status = 'primary'
    href = None
    target = None
    modal_target = True

    permission = None

    css_classes = {
        'th': 'action',
        'td': 'action'
    }

    def is_visible(self, item):
        """Action visibility checker"""
        if not self.has_permission(item):
            return False
        if self.checker:
            if callable(self.checker):
                checked = self.checker(item)  # pylint: disable=not-callable
            else:
                checked = self.checker
            if not checked:
                return False
        return True

    def get_url(self, item):
        """Action URL getter"""
        return absolute_url(item, self.request, self.href)


class ActionColumn(ProtectedViewObjectMixin, BaseActionColumn):
    """Base action column

    This column class inherits from :py:class:`ProtectedViewObjectMixin
    <pyams_security.security.ProtectedViewObjectMixin>`, so you can use adapters
    to define permission required to enable this action.
    """

    def render_cell(self, item):
        """Column cell renderer"""
        if not self.is_visible(item):
            return ''
        return '<a href="{}" ' \
               '   data-ams-stop-propagation="true" ' \
               '   {} {} {}>{}</a>'.format(
                self.get_url(item),
                'data-ams-target="{}"'.format(self.target) if self.target else '',
                'data-toggle="modal"' if self.modal_target else '',
                'data-ams-modules="modal"' if self.modal_target else '',
                self.get_icon(item))


class ButtonColumn(BaseActionColumn):
    """Button action column"""

    label = None

    css_classes = {
        'th': 'action',
        'td': 'action py-1'
    }

    def render_cell(self, item):
        """Column cell renderer"""
        if not self.is_visible(item):
            return ''
        return '<a class="btn btn-sm btn-{} text-nowrap" ' \
               '   href="{}" ' \
               '   data-ams-stop-propagation="true" ' \
               '   {} {} {}>{}</a>'.format(
                self.status,
                self.get_url(item),
                'data-ams-target="{0}"'.format(self.target) if self.target else '',
                'data-toggle="modal"' if self.modal_target else '',
                'data-ams-modules="modal"' if self.modal_target else '',
                self.request.localizer.translate(self.label))


class JsActionColumn(ActionColumn):
    """Javascript action column"""

    def get_url(self, item):
        """Action URL getter"""
        return self.href


class AttributeSwitcherColumn(ObjectDataManagerMixin, JsActionColumn):
    """Attribute switcher column"""

    href = 'MyAMS.container.switchElementAttribute'
    modal_target = False

    attribute_name = None
    attribute_switcher = None

    icon_on_class = 'far fa-eye'
    icon_off_class = 'far fa-eye-slash'

    @property
    def object_data(self):
        """Object data getter"""
        return {
            'ams-modules': 'container',
            'ams-update-target': self.attribute_switcher,
            'ams-attribute-name': self.attribute_name,
            'ams-icon-on': self.icon_on_class,
            'ams-icon-off': self.icon_off_class
        }

    def get_icon_class(self, item):
        """Icon class getter"""
        return self.icon_on_class if getattr(item, self.attribute_name) else self.icon_off_class

    def render_cell(self, item):
        """Cell renderer"""
        if self.has_permission(item):
            return super().render_cell(item)
        return f'<span class="hint" data-original-title="{self.get_icon_hint(item)}">' \
               f'{self.get_icon(item)}' \
               f'</span>'


class VisibilityColumn(AttributeSwitcherColumn):
    """Visibility switcher column"""

    attribute_name = 'visible'
    attribute_switcher = 'switch-visible-item.json'

    weight = 1

    def get_icon_hint(self, item):
        """Icon hint getter"""
        if self.has_permission(item):
            hint = _("Click to show/hide item")
        elif item.visible:
            hint = _("This element is visible")
        else:
            hint = _("This element is not visible")
        return self.request.localizer.translate(hint)


class TrashColumn(ObjectDataManagerMixin, JsActionColumn):
    """Trash column"""

    hint = _("Delete element")
    icon_class = 'fa fa-trash-alt'

    action_type = 'delete'

    href = 'MyAMS.container.deleteElement'
    modal_target = False

    object_data = {
        'ams-modules': 'container'
    }

    weight = 999

    def has_permission(self, item):
        """Column permission checker"""
        request = self.request
        checker = get_permission_checker(request, item, action=self.action_type)
        permission = checker.edit_permission if checker is not None else None
        if permission is not None:
            return request.has_permission(permission, context=item)
        return super().has_permission(item)


class DateColumn(GetAttrColumn):
    """Date or datetime column"""

    formatter = SH_DATE_FORMAT

    def get_value(self, obj):
        """Date column value getter"""
        value = super().get_value(obj)
        if not value:
            return '--'
        return format_datetime(value, self.formatter, self.request)


@implementer(ITableElementEditor)
class TableElementEditor(ContextRequestViewAdapter):
    """Base table element editor"""

    view_name = FieldProperty(ITableElementEditor['view_name'])
    modal_target = FieldProperty(ITableElementEditor['modal_target'])

    @property
    def href(self):
        """Table element editor getter"""
        return absolute_url(self.context, self.request, self.view_name)
