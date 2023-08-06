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

"""PyAMS_zmi.zmi.timezone module

This modules defines views which are used to get access to PyAMS server timezone utility.
"""

from zope.interface import Interface

from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import MANAGE_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.timezone import IServerTimezone
from pyams_zmi.form import AdminModalEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.table import TableElementEditor


__docformat__ = 'restructuredtext'

from pyams_zmi import _


@adapter_config(required=(IServerTimezone, IAdminLayer, Interface),
                provides=ITableElementEditor)
class ServerTimezoneEditor(TableElementEditor):
    """Server timezone editor adapter"""


@ajax_form_config(name='properties.html', context=IServerTimezone, layer=IPyAMSLayer)
class ServerTimezonePropertiesEditForm(AdminModalEditForm):
    """Server timezone properties edit form"""

    title = _("Server timezone")
    legend = _("Properties")

    fields = Fields(IServerTimezone)

    _edit_permission = MANAGE_SYSTEM_PERMISSION
