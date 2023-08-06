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

"""PyAMS_zmi.helper.event module

This module provides a few set of helpers which can be used to render JSON results which
can be used by MyAMS to refresh elements.
"""

from datetime import datetime

from zope.component import getMultiAdapter
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import alsoProvides

from pyams_form.interfaces.form import IContextAware, IFormAware
from pyams_form.interfaces.widget import IFieldWidget
from pyams_form.util import expand_prefix
from pyams_utils.factory import get_object_factory, is_interface
from pyams_utils.url import absolute_url
from pyams_zmi.table import get_table_id


__docformat__ = 'restructuredtext'


def get_json_image_refresh_callback(image, image_id, request):
    """Get image refresh callback settings"""
    dc = IZopeDublinCore(image, None)  # pylint: disable=invalid-name
    if dc is None:
        timestamp = datetime.utcnow().timestamp()
    else:
        timestamp = dc.modified.timestamp()  # pylint: disable=no-member
    return {
        'module': 'helpers',
        'callback': 'MyAMS.helpers.refreshImage',
        'options': {
            'image_id': image_id,
            'src': '{}?_={}'.format(absolute_url(image, request), timestamp)
        }
    }


def get_json_widget_refresh_callback(form, field_name, request=None):
    """Get widget refresh callback settings"""
    field = form.fields[field_name]
    factory = field.widget_factory.get(form.mode)
    if request is None:
        request = form.request
    if factory is not None:
        widget = factory(field.field, request)
    else:
        widget = getMultiAdapter((field.field, request), IFieldWidget)
    widget.name = expand_prefix(form.prefix) + expand_prefix(form.widgets.prefix) + field.__name__
    widget.id = widget.name.replace('.', '-')
    widget.form = form
    widget.context = form.get_content()
    widget.mode = form.mode
    widget.ignore_request = True
    widget.ignore_context = False
    alsoProvides(widget, IFormAware)
    alsoProvides(widget, IContextAware)
    widget.update()
    return {
        'module': 'helpers',
        'callback': 'MyAMS.helpers.refreshWidget',
        'options': {
            'widget_id': widget.id,
            'content': widget()
        }
    }


def get_json_table_refresh_callback(context, request, table_factory):
    """Get table refresh callback settings"""
    factory = get_object_factory(table_factory) if is_interface(table_factory) else table_factory
    table = factory(context, request)
    table.update()
    return {
        'module': 'helpers',
        'callback': 'MyAMS.helpers.refreshElement',
        'options': {
            'object_id': get_table_id(table),
            'content': table.render()
        }
    }


def get_json_table_row_add_callback(context, request, table_factory, item):
    """Get table row add callback settings"""
    factory = get_object_factory(table_factory) if is_interface(table_factory) else table_factory
    table = factory(context, request)
    table.update()
    row = table.setup_row(item)
    return {
        'module': 'helpers',
        'callback': 'MyAMS.helpers.addTableRow',
        'options': {
            'table_id': get_table_id(table),
            'row_id': table.get_row_id(item),
            'content': table.render_row(row)
        }
    }


def get_json_table_row_refresh_callback(context, request, table_factory, item):
    """Get table row refresh callback settings"""
    factory = get_object_factory(table_factory) if is_interface(table_factory) else table_factory
    table = factory(context, request)
    table.update()
    row = table.setup_row(item)
    return {
        'module': 'helpers',
        'callback': 'MyAMS.helpers.refreshTableRow',
        'options': {
            'row_id': table.get_row_id(item),
            'data': table.render_row(row)
        }
    }
