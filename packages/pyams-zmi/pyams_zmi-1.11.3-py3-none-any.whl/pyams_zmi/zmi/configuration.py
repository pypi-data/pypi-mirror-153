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

"""PyAMS_zmi.configuration module

This module provides views and content providers used to handle ZMI configuration.
"""

from zope.interface import Interface

from pyams_form.ajax import ajax_form_config
from pyams_form.browser.checkbox import SingleCheckBoxFieldWidget
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces.form import IAJAXFormRenderer, IGroup
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import MANAGE_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_skin.interfaces.viewlet import IHelpViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.configuration import IZMIConfiguration
from pyams_zmi.zmi.interfaces import IConfigurationMenu
from pyams_zmi.interfaces.viewlet import IControlPanelMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_zmi import _


@adapter_config(required=(ISiteRoot, IAdminLayer, Interface),
                provides=IObjectLabel)
def site_root_label(context, request, view):
    """Site root label getter"""
    configuration = IZMIConfiguration(context)
    i18n = II18n(configuration)
    return i18n.query_attribute('home_name', request=request) or \
        i18n.query_attribute('site_name', request=request) or \
        request.localizer.translate(_("Home"))


@viewletmanager_config(name='configuration.menu', context=ISiteRoot, layer=IAdminLayer,
                       manager=IControlPanelMenu, weight=10, permission=MANAGE_SYSTEM_PERMISSION,
                       provides=IConfigurationMenu)
class ConfigurationMenu(NavigationMenuItem):
    """Configuration menu"""

    label = _("Configuration")
    icon_class = 'fas fa-sliders-h'


@viewletmanager_config(name='zmi-configuration.menu', context=ISiteRoot, layer=IAdminLayer,
                       manager=IConfigurationMenu, weight=10, permission=MANAGE_SYSTEM_PERMISSION)
class ZMIConfigurationMenu(NavigationMenuItem):
    """ZMI configuration menu"""

    label = _("ZMI configuration")

    href = '#zmi-configuration.html'


@ajax_form_config(name='zmi-configuration.html', context=ISiteRoot, layer=IPyAMSLayer,
                  permission=MANAGE_SYSTEM_PERMISSION)
class ZMIConfigurationForm(AdminEditForm):
    """ZMI configuration form"""

    title = _("ZMI configuration")
    legend = _("Interface configuration")

    fields = Fields(IZMIConfiguration).select('site_name', 'home_name',
                                              'application_name', 'application_package',
                                              'inner_package_name', 'inner_package',
                                              'environment', 'favicon', 'myams_bundle')

    def get_content(self):
        return IZMIConfiguration(self.context)


@adapter_config(required=(ISiteRoot, IAdminLayer, ZMIConfigurationForm),
                provides=IAJAXFormRenderer)
class ZMIConfigurationFormRenderer(ContextRequestViewAdapter):
    """ZMI configuration AJAX form renderer"""

    def render(self, changes):
        """ZMI configuration form renderer"""
        if not changes:
            return {
                'status': 'info',
                'message': self.request.localizer.translate(self.view.no_changes_message)
            }
        return {
            'status': 'redirect'
        }


@adapter_config(name='zmi-profile',
                required=(ISiteRoot, IAdminLayer, ZMIConfigurationForm),
                provides=IGroup)
class ZMIConfigurationProfileGroup(FormGroupChecker):
    """ZMI configuration profile fields"""

    fields = Fields(IZMIConfiguration).select('user_bundle_selection', 'user_bundles')

    weight = 5


@adapter_config(name='zmi-header',
                required=(ISiteRoot, IAdminLayer, ZMIConfigurationForm),
                provides=IGroup)
class ZMIConfigurationHeaderGroup(FormGroupChecker):
    """ZMI configuration header fields"""

    fields = Fields(IZMIConfiguration).select('include_header', 'fixed_header', 'logo')
    # fields['fixed_header'].widget_factory = SingleCheckBoxFieldWidget

    weight = 10


@adapter_config(name='zmi-search',
                required=(ISiteRoot, IAdminLayer, ZMIConfigurationForm),
                provides=IGroup)
class ZMIConfigurationSearchGroup(FormGroupChecker):
    """ZMI configuration search fields"""

    fields = Fields(IZMIConfiguration).select('include_site_search', 'site_search_placeholder',
                                              'site_search_handler')

    weight = 20


@adapter_config(name='zmi-navigation',
                required=(ISiteRoot, IAdminLayer, ZMIConfigurationForm),
                provides=IGroup)
class ZMIConfigurationNavigationGroup(FormGroupChecker):
    """ZMI configuration navigation fields"""

    fields = Fields(IZMIConfiguration).select('include_menus', 'include_minify_button',
                                              'fixed_navigation', 'accordion_menus')
    fields['include_minify_button'].widget_factory = SingleCheckBoxFieldWidget
    fields['fixed_navigation'].widget_factory = SingleCheckBoxFieldWidget
    fields['accordion_menus'].widget_factory = SingleCheckBoxFieldWidget

    weight = 30


@viewlet_config(name='zmi-navigation-warning', context=ISiteRoot,
                layer=IAdminLayer, view=ZMIConfigurationNavigationGroup,
                manager=IHelpViewletManager)
class NavigationAlertMessage(AlertMessage):
    """Navigation alert message"""

    status = 'danger'
    icon_class = 'fas fa-exclamation-triangle'
    header = _("Warning!")
    _message = _("""Removing navigation menus will also remove access to this form...""")


@adapter_config(name='zmi-ribbon',
                required=(ISiteRoot, IAdminLayer, ZMIConfigurationForm),
                provides=IGroup)
class ZMIConfigurationRibbonGroup(FormGroupChecker):
    """ZMI configuration ribbon fields"""

    fields = Fields(IZMIConfiguration).select('include_ribbon', 'fixed_ribbon')
    fields['fixed_ribbon'].widget_factory = SingleCheckBoxFieldWidget

    weight = 40


@adapter_config(name='zmi-misc',
                required=(ISiteRoot, IAdminLayer, ZMIConfigurationForm),
                provides=IGroup)
class ZMIConfigurationMiscGroup(Group):
    """ZMI configuration misc fields"""

    legend = _("Custom extensions")

    fields = Fields(IZMIConfiguration).select('custom_stylesheet', 'base_body_css_class',
                                              'custom_script')

    weight = 50
