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

"""PyAMS_zmi.resources module

This module defines a custom adapter which is used to get access to custom CSS and Javascript
resources which can be defined in PyAMS ZMI configuration.

This modules also defines the MyAMS bundle which is used for management interface.
"""

from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface

from pyams_layer.interfaces import IResources
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.fanstatic import ExternalResource
from pyams_utils.url import absolute_url
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.configuration import IZMIConfiguration, MYAMS_BUNDLES


__docformat__ = 'restructuredtext'

from pyams_zmi.interfaces.profile import IUserProfile


@adapter_config(required=(Interface, IAdminLayer, Interface),
                provides=IResources)
class ZMIResourcesAdapter(ContextRequestViewAdapter):
    """ZMI resources adapter"""

    weight = 10

    @property
    def resources(self):
        """Resources getter"""
        request = self.request
        configuration = IZMIConfiguration(request.root, None)
        if configuration is not None:
            # yield main bundle
            bundle = None
            if configuration.user_bundle_selection:
                profile = IUserProfile(self.request.principal, None)
                if profile is not None:
                    bundle, _label = MYAMS_BUNDLES.get(profile.zmi_bundle, (None, None))
            if bundle is None:
                bundle, _label = MYAMS_BUNDLES.get(configuration.myams_bundle)
            yield bundle
            # yield stylesheet
            stylesheet = configuration.custom_stylesheet
            if stylesheet:
                modified = IZopeDublinCore(stylesheet).modified
                stylesheet_url = absolute_url(stylesheet, request,
                                              query={'_': modified.timestamp()})  # pylint: disable=no-member
                resource = bundle.library.known_resources.get(stylesheet_url)
                if resource is None:
                    resource = ExternalResource(bundle.library, stylesheet_url,
                                                resource_type='css',
                                                depends=(bundle,))
                yield resource
            # yield script
            script = configuration.custom_script
            if script:
                modified = IZopeDublinCore(script).modified
                script_url = absolute_url(script, request,
                                          query={'_': modified.timestamp()})  # pylint: disable=no-member
                resource = bundle.library.known_resources.get(script_url)
                if resource is None:
                    resource = ExternalResource(bundle.library, script_url,
                                                resource_type='js',
                                                depends=(bundle,))
                yield resource
