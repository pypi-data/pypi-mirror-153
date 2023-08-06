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

"""PyAMS_zmi.interfaces.form module

This module provides public interfaces for management forms.
"""

from zope.interface import Attribute, Interface
from zope.schema import Choice, TextLine

from pyams_form.interfaces import INPUT_MODE
from pyams_form.interfaces.form import IDisplayForm, IForm, IGroup, IInnerSubForm, IInnerTabForm
from pyams_skin.schema.button import CloseButton, ResetButton, SubmitButton
from pyams_template.template import override_template, template_config
from pyams_zmi.interfaces import IAdminLayer


__docformat__ = 'restructuredtext'

from pyams_zmi import _


override_template(IForm, template='templates/form.pt', layer=IAdminLayer)
override_template(IDisplayForm, template='templates/form-display.pt', layer=IAdminLayer)

override_template(IGroup, template='templates/form-group.pt', layer=IAdminLayer)

override_template(IInnerSubForm, template='templates/form-group.pt', layer=IAdminLayer)

override_template(IInnerTabForm, template='templates/form-tabform.pt', layer=IAdminLayer)


class IFormTitle(Interface):
    """Form title getter interface"""


def check_submit_button(form):
    """Submit button checker"""
    if form.mode != INPUT_MODE:
        return False
    for subform in form.get_forms():
        for widget in (subform.widgets or {}).values():
            if widget.mode == INPUT_MODE:
                return True
    return False


class IAddFormButtons(Interface):
    """Add forms buttons interface"""

    add = SubmitButton(name='add',
                       title=_("Add"),
                       condition=check_submit_button)

    cancel = ResetButton(name='reset',
                         title=_("Reset"))


class IModalAddFormButtons(Interface):
    """Modal add forms buttons interface"""

    add = SubmitButton(name='add',
                       title=_("Add"),
                       condition=check_submit_button)

    close = CloseButton(name='close',
                        title=_("Cancel"))


class IEditFormButtons(Interface):
    """Edit forms buttons interface"""

    apply = SubmitButton(name='apply',
                         title=_("Apply"),
                         condition=check_submit_button)

    cancel = ResetButton(name='reset',
                         title=_("Reset"))


class IModalEditFormButtons(Interface):
    """Modal edit forms buttons interface"""

    apply = SubmitButton(name='apply',
                         title=_("Apply"),
                         condition=check_submit_button)

    close = CloseButton(name='close',
                        title=_("Cancel"))


class IDisplayFormButtons(Interface):
    """Display forms buttons interface"""


class IModalDisplayFormButtons(Interface):
    """Modal display forms buttons interface"""

    close = CloseButton(name='close',
                        title=_("Cancel"))


@template_config(template='templates/form-switcher.pt', layer=IAdminLayer)
class IFormGroupSwitcher(IGroup):
    """Form group switcher interface"""

    minus_class = TextLine(title="Expanded switcher FontAwesome CSS class (without prefix)",
                           default='minus')

    plus_class = TextLine(title="Reduced switcher FontAwesome CSS class (without prefix)",
                          default='plus')

    switcher_mode = Choice(title="Switcher display mode",
                           values=('always', 'never', 'auto'),
                           default='auto')

    state = Attribute("Initial switcher state")


@template_config(template='templates/form-checker.pt', layer=IAdminLayer)
class IFormGroupChecker(IGroup):
    """Form group checker interface"""

    checker_fieldname = TextLine(title="Checker checkbox field name")

    checker_widget = Attribute("Checker checkbox field")

    checker_mode = Choice(title="Checker display mode",
                          values=('hide', 'disable'),
                          default='hide')

    checker_state = Attribute("Initial switcher state")


@template_config(template='templates/search-view.pt', layer=IAdminLayer)
class ISearchView(Interface):
    """Base search view interface"""

    search_factory = Attribute("Search form interface")

    search_form = Attribute("Search form view")


class ISearchInfo(Interface):
    """Base search interface"""

    query = TextLine(title=_("Search for"))


class ISearchButtons(Interface):
    """Search form buttons interface"""

    search = SubmitButton(name='search', title=_("Search"))

    cancel = ResetButton(name='reset', title=_("Reset"))
