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

This module provides support for basic management interface configuration based on MyAMS
features.
"""

import pkg_resources
from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_file.property import FileProperty
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_security.interfaces.base import MANAGE_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteEtcTraverser, ISiteRoot
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config, \
    get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_utils.request import query_request
from pyams_utils.vocabulary import vocabulary_config
from pyams_zmi.interfaces.configuration import IZMIConfiguration, MYAMS_BUNDLES, \
    USER_BUNDLES_VOCABULARY


__docformat__ = 'restructuredtext'


@factory_config(IZMIConfiguration)
class ZMIConfiguration(Persistent, Contained):
    """ZMI configuration class"""

    site_name = FieldProperty(IZMIConfiguration['site_name'])
    home_name = FieldProperty(IZMIConfiguration['home_name'])
    application_name = FieldProperty(IZMIConfiguration['application_name'])
    application_package = FieldProperty(IZMIConfiguration['application_package'])
    inner_package_name = FieldProperty(IZMIConfiguration['inner_package_name'])
    inner_package = FieldProperty(IZMIConfiguration['inner_package'])
    environment = FieldProperty(IZMIConfiguration['environment'])

    @property
    def version(self):
        """Get complete version string"""
        result = pkg_resources.get_distribution(self.application_package).version
        if self.inner_package and (self.inner_package != self.application_package):
            result = '{}<span class="mx-2">&ndash;</span>{} - {}'.format(
                result,
                self.inner_package_name,
                pkg_resources.get_distribution(self.inner_package).version)
        return result

    myams_bundle = FieldProperty(IZMIConfiguration['myams_bundle'])
    user_bundle_selection = FieldProperty(IZMIConfiguration['user_bundle_selection'])
    user_bundles = FieldProperty(IZMIConfiguration['user_bundles'])

    favicon = FileProperty(IZMIConfiguration['favicon'])

    include_header = FieldProperty(IZMIConfiguration['include_header'])
    fixed_header = FieldProperty(IZMIConfiguration['fixed_header'])
    logo = FileProperty(IZMIConfiguration['logo'])

    include_site_search = FieldProperty(IZMIConfiguration['include_site_search'])
    site_search_placeholder = FieldProperty(IZMIConfiguration['site_search_placeholder'])
    site_search_handler = FieldProperty(IZMIConfiguration['site_search_handler'])

    include_menus = FieldProperty(IZMIConfiguration['include_menus'])
    include_minify_button = FieldProperty(IZMIConfiguration['include_minify_button'])
    fixed_navigation = FieldProperty(IZMIConfiguration['fixed_navigation'])
    accordion_menus = FieldProperty(IZMIConfiguration['accordion_menus'])

    include_ribbon = FieldProperty(IZMIConfiguration['include_ribbon'])
    fixed_ribbon = FieldProperty(IZMIConfiguration['fixed_ribbon'])

    base_body_css_class = FieldProperty(IZMIConfiguration['base_body_css_class'])

    @property
    def body_css_class(self):
        """Body CSS class getter"""
        result = self.base_body_css_class or ''
        for attr in ('header', 'navigation', 'ribbon'):
            if getattr(self, 'fixed_' + attr, False):
                result += ' fixed-' + attr
        return result

    custom_stylesheet = FileProperty(IZMIConfiguration['custom_stylesheet'])
    custom_script = FileProperty(IZMIConfiguration['custom_script'])


@adapter_config(required=IZMIConfiguration, provides=IViewContextPermissionChecker)
class ZMIConfigurationPermissionChecker(ContextAdapter):
    """ZMI configuration permission checker"""

    edit_permission = MANAGE_SYSTEM_PERMISSION


ZMI_CONFIGURATION_KEY = 'pyams_zmi.configuration'
"""Annotations key used to store ZMI configuration"""


@adapter_config(required=ISiteRoot, provides=IZMIConfiguration)
def zmi_configuration_factory(context):
    """ZMI configuration factory"""
    return get_annotation_adapter(context, ZMI_CONFIGURATION_KEY, IZMIConfiguration,
                                  notify=False, name='++etc++zmi.configuration')


@adapter_config(name='zmi.configuration', required=ISiteRoot, provides=ISiteEtcTraverser)
def site_root_zmi_configuration_traverser(context):
    """Site root ++etc++zmi.configuration traverser extension"""
    return IZMIConfiguration(context, None)


@adapter_config(name='zmi.configuration',
                required=(Interface, Interface, Interface),
                provides=ITALESExtension)
class ZMIConfigurationTalesExtension(ContextRequestViewAdapter):
    """zmi.configuration TALES extension"""

    def render(self, context=None):  # pylint: disable=unused-argument
        """TALES extension renderer"""
        return IZMIConfiguration(self.request.root, None)


@vocabulary_config(USER_BUNDLES_VOCABULARY)
class UserBundlesVocabulary(SimpleVocabulary):
    """User bundles vocabulary"""

    def __init__(self, context=None):
        terms = []
        request = query_request()
        if request is not None:
            configuration = IZMIConfiguration(request.root)
            terms = [
                SimpleTerm(v, title=MYAMS_BUNDLES[v][1])
                for v in configuration.user_bundles or ()
            ]
        super().__init__(terms)
