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

"""PyAMS_zmi.form module

This module provides all base form-related classes to be used into PyAMS management
interface.
"""

from pyramid.decorator import reify
from zope.interface import Interface, implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_form.browser.checkbox import SingleCheckBoxFieldWidget
from pyams_form.button import Buttons, handler
from pyams_form.form import AddForm, DisplayForm, EditForm
from pyams_form.group import Group, GroupForm, GroupManager
from pyams_form.interfaces import DISPLAY_MODE
from pyams_form.subform import InnerAddForm, InnerDisplayForm, InnerEditForm
from pyams_i18n.schema import II18nField
from pyams_skin.interfaces.view import IInnerPage, IModalPage
from pyams_utils.adapter import query_adapter
from pyams_utils.data import ObjectDataManagerMixin
from pyams_zmi.interfaces.form import IAddFormButtons, IDisplayFormButtons, IEditFormButtons, \
    IFormGroupChecker, IFormGroupSwitcher, IFormTitle, IModalAddFormButtons, \
    IModalDisplayFormButtons, \
    IModalEditFormButtons
from pyams_zmi.view import AdminView


__docformat__ = 'restructuredtext'


class BaseFormMixin:
    """Base form mixin class"""

    @property
    def title(self):
        """Title getter"""
        title = query_adapter(IFormTitle, self.request, self.context, self)
        return title or super().title


#
# Base add forms
#

# pylint: disable=abstract-method
@implementer(IInnerPage)
class AdminAddForm(ObjectDataManagerMixin, BaseFormMixin,
                   GroupForm, AddForm, AdminView):
    """Management add form"""

    @property
    def buttons(self):
        """Default add form buttons getter"""
        if self.mode == DISPLAY_MODE:
            return Buttons(Interface)
        return Buttons(IAddFormButtons)

    @handler(IAddFormButtons['add'])
    def handle_add(self, action):
        """Default add form button handler"""
        super().handle_add(self, action)  # pylint: disable=too-many-function-args


@implementer(IModalPage)
class AdminModalAddForm(AdminAddForm):
    """Modal management add form"""

    @property
    def buttons(self):
        if self.mode == DISPLAY_MODE:
            return Buttons(IModalDisplayFormButtons)
        return Buttons(IModalAddFormButtons)

    modal_class = FieldProperty(IModalPage['modal_class'])
    ajax_form_target = None

    @handler(IModalAddFormButtons['add'])
    def handle_add(self, action):
        super().handle_add(self, action)  # pylint: disable=too-many-function-args


@implementer(IInnerPage)
class AdminInnerAddForm(ObjectDataManagerMixin, BaseFormMixin,
                        GroupForm, InnerAddForm, AdminView):
    """Inner management add form"""

    buttons = Buttons(Interface)


#
# Base edit forms
#

@implementer(IInnerPage)
class AdminEditForm(ObjectDataManagerMixin, BaseFormMixin,
                    GroupForm, EditForm, AdminView):
    """Management edit form"""

    @property
    def buttons(self):
        """Default inner page buttons getter"""
        if self.mode == DISPLAY_MODE:
            return Buttons(Interface)
        return Buttons(IEditFormButtons)

    @handler(IEditFormButtons['apply'])
    def handle_apply(self, action):
        super().handle_apply(self, action)  # pylint: disable=too-many-function-args


@implementer(IModalPage)
class AdminModalEditForm(AdminEditForm):
    """Modal management edit form"""

    @property
    def buttons(self):
        if self.mode == DISPLAY_MODE:
            return Buttons(IModalDisplayFormButtons)
        return Buttons(IModalEditFormButtons)

    modal_class = FieldProperty(IModalPage['modal_class'])
    ajax_form_target = None

    @handler(IModalEditFormButtons['apply'])
    def handle_apply(self, action):
        super().handle_apply(self, action)  # pylint: disable=too-many-function-args


@implementer(IInnerPage)
class AdminInnerEditForm(ObjectDataManagerMixin, BaseFormMixin,
                         GroupForm, InnerEditForm, AdminView):
    """Inner management edit form"""

    buttons = Buttons(Interface)


#
# Base display forms
#

@implementer(IInnerPage)
class AdminDisplayForm(ObjectDataManagerMixin, BaseFormMixin,
                       GroupManager, DisplayForm, AdminView):
    """Management display form"""

    buttons = Buttons(IDisplayFormButtons)


@implementer(IModalPage)
class AdminModalDisplayForm(AdminDisplayForm):
    """Modal management display form"""

    buttons = Buttons(IModalDisplayFormButtons)

    modal_class = FieldProperty(IModalPage['modal_class'])


@implementer(IInnerPage)
class AdminInnerDisplayForm(ObjectDataManagerMixin, BaseFormMixin,
                            GroupForm, InnerDisplayForm, AdminView):
    """Inner management display form"""

    buttons = Buttons(Interface)


#
# Switcher group
#

@implementer(IFormGroupSwitcher)
class FormGroupSwitcher(ObjectDataManagerMixin, Group):
    """Form group switcher

    A "group switcher" is based on a "switcher" component provided by MyAMS, which allows to
    switch a whole fieldset.
    """

    minus_class = FieldProperty(IFormGroupSwitcher['minus_class'])
    plus_class = FieldProperty(IFormGroupSwitcher['plus_class'])
    switcher_mode = FieldProperty(IFormGroupSwitcher['switcher_mode'])

    @property
    def state(self):
        """Current state getter"""
        if self.switcher_mode == 'always':
            return 'open'
        if self.switcher_mode == 'never':
            return 'closed'
        # else: automatic mode
        for widget in self.widgets.values():
            if widget.ignore_context:
                continue
            field = widget.field
            if self.ignore_context:
                value = field.default
            else:
                context = widget.context
                name = field.getName()
                value = getattr(field.interface(context), name, None)
            if value and (value != field.default):
                if II18nField.providedBy(field):  # pylint: disable=no-value-for-parameter
                    for i18n_value in value.values():
                        if i18n_value:
                            return 'open'
                return 'open'
        return 'closed'


#
# Checker group
#

@implementer(IFormGroupChecker)
class FormGroupChecker(ObjectDataManagerMixin, Group):
    """Form group checker

    A "group checker" is based on a "checker" component provided by MyAMS, which allows to
    hide or disable a whole fieldset with a checkbox matching a form's field value.
    """

    checker_fieldname = FieldProperty(IFormGroupChecker['checker_fieldname'])
    checker_mode = FieldProperty(IFormGroupChecker['checker_mode'])

    def __init__(self, context, request, parent_form):
        super().__init__(context, request, parent_form)
        name, field = next(iter(self.fields.items()))
        self.checker_fieldname = name
        self.legend = field.field.title
        self.fields[self.checker_fieldname].widget_factory = SingleCheckBoxFieldWidget

    @reify
    def checker_widget(self):
        """Checker widget getter"""
        return self.widgets[self.checker_fieldname]

    @property
    def checker_state(self):
        """Checker state getter"""
        return 'on' if 'selected' in self.checker_widget.value else 'off'
