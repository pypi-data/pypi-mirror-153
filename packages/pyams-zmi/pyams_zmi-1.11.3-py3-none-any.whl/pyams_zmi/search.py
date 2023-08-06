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

"""PyAMS_zmi.search module

This module provides a little set of base classes which can be used in search forms.
"""

from pyramid.interfaces import IView
from zope.interface import Interface, implementer

from pyams_form.button import Buttons
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields
from pyams_pagelet.pagelet import Pagelet
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import get_object_factory, is_interface
from pyams_zmi.form import AdminAddForm
from pyams_zmi.interfaces import IAdminLayer, IPageTitle
from pyams_zmi.interfaces.form import ISearchButtons, ISearchInfo, ISearchView
from pyams_zmi.table import TableAdminView
from pyams_zmi.view import InnerAdminView


__docformat__ = 'restructuredtext'

from pyams_zmi import _  # pylint: disable=ungrouped-imports


# pylint: disable=abstract-method
class SearchForm(AdminAddForm):
    """Base search form"""

    title = _("Search form")
    legend = _("Search criteria")

    buttons = Buttons(ISearchButtons)

    ajax_form_handler = 'search-results.html'
    ajax_form_target = '#search-results'


@adapter_config(required=(Interface, IAdminLayer, SearchForm),
                provides=IFormFields)
def search_form_fields(context, request, form):
    """Search form fields getter"""
    return Fields(ISearchInfo)


@implementer(ISearchView)
class SearchView(InnerAdminView):
    """Base search view"""

    search_form = SearchForm

    def __init__(self, context, request):
        super().__init__(context, request)
        factory = get_object_factory(self.search_form) if is_interface(self.search_form) \
            else self.search_form
        self.search_form = factory(context, request)

    def update(self):
        """Search view update"""
        super().update()  # pylint: disable=no-member
        self.search_form.update()


@implementer(IView)
class SearchResultsView(TableAdminView, Pagelet):
    """Search results view"""

    title = None


@adapter_config(required=(Interface, IAdminLayer, SearchResultsView),
                provides=IPageTitle)
def search_results_title(context, request, view):  # pylint: disable=unused-argument
    """Search results view title adapter"""
    return ' '
