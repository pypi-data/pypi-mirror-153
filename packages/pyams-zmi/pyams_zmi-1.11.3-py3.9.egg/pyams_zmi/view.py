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

"""PyAMS_zmi.view module

This module provides generic management views features.
"""

from pyramid.events import subscriber
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_form.interfaces.form import IFormCreatedEvent
from pyams_layer.skin import apply_skin
from pyams_pagelet.interfaces import IPageletCreatedEvent
from pyams_utils.adapter import get_adapter_weight
from pyams_zmi.interfaces import IAdminView, ICompositeView, IInnerAdminView, \
    PYAMS_ADMIN_SKIN_NAME


__docformat__ = 'restructuredtext'


@implementer(IAdminView)
class AdminView:
    """Base admin view"""

    header_label = FieldProperty(IAdminView['header_label'])


@subscriber(IPageletCreatedEvent, context_selector=IAdminView)
def handle_admin_view(event):
    """Automatically apply admin skin to admin views"""
    apply_skin(event.request, PYAMS_ADMIN_SKIN_NAME)


@subscriber(IFormCreatedEvent, context_selector=IAdminView)
def handle_admin_form(event):
    """Automatically apply admin skin to admin forms"""
    apply_skin(event.object.request, PYAMS_ADMIN_SKIN_NAME)


@implementer(IInnerAdminView)
class InnerAdminView(AdminView):
    """Inner admin view"""

    title = FieldProperty(IInnerAdminView['title'])


class CompositeAdminView(InnerAdminView):
    """Composite admin view"""

    @property
    def views(self):
        """Inner views getter"""
        registry = self.request.registry
        for name, view in sorted(registry.getAdapters((self.context, self.request, self),
                                                      ICompositeView),
                                 key=get_adapter_weight):
            view.update()
            yield view

    def render(self):
        """View renderer"""
        return ''.join((
            view.render()
            for view in self.views
        ))
