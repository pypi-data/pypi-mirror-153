#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_zmi.profile module

This module provides custom ZMI-related user settings.
"""

__docformat__ = 'restructuredtext'

from persistent import Persistent
from pyramid.security import ALL_PERMISSIONS, Allow, Everyone
from pyramid.threadlocal import get_current_request
from zope.container.contained import Contained
from zope.interface import Interface
from zope.intid import IIntIds
from zope.location import locate
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import ITraversable

from pyams_file.image import get_image_selection
from pyams_file.property import FileProperty
from pyams_security.interfaces.base import IPrincipalInfo, PUBLIC_PERMISSION
from pyams_security.interfaces.names import ADMIN_USER_ID
from pyams_utils.adapter import ContextRequestAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_utils.registry import get_utility
from pyams_utils.request import check_request, query_request
from pyams_zmi.interfaces.profile import IUserProfile, USER_PROFILE_KEY


@factory_config(IUserProfile)
class UserProfile(Persistent, Contained):
    """User profile persistent class"""

    avatar = FileProperty(IUserProfile['avatar'])
    zmi_bundle = FieldProperty(IUserProfile['zmi_bundle'])

    @staticmethod
    def __acl__():
        result = [(Allow, ADMIN_USER_ID, ALL_PERMISSIONS)]
        request = query_request()
        if request is not None:
            result.append((Allow, request.principal.id, ALL_PERMISSIONS))
        result.append((Allow, Everyone, PUBLIC_PERMISSION))
        return result

    def get_avatar(self, selection='square', size='32x32', request=None):
        """Avatar URL getter"""
        if self.avatar:
            return get_image_selection(self.avatar, selection, size, request)
        return None


@adapter_config(required=IPrincipalInfo,
                provides=IUserProfile)
def principal_user_profile_factory(principal):
    """Principal user profile factory adapter"""

    def user_profile_callback(profile):
        request = get_current_request()
        if request is not None:
            root = request.root
            intids = get_utility(IIntIds)
            locate(profile, root)  # avoid NotYet exception
            locate(profile, root, '++profile++{0}'.format(intids.register(profile)))

    return get_annotation_adapter(principal, USER_PROFILE_KEY, IUserProfile,
                                  locate=False, callback=user_profile_callback)


@adapter_config(required=Interface,
                provides=IUserProfile)
def user_profile_factory(context):
    request = check_request()
    return IUserProfile(request.principal)


@adapter_config(name='profile',
                required=(Interface, Interface),
                provides=ITraversable)
class UserProfileTraverser(ContextRequestAdapter):
    """++profile++ namespace traverser"""

    def traverse(self, name, furtherpath=None):
        if not name:
            return IUserProfile(self.request.principal)
        intids = get_utility(IIntIds)
        profile = intids.queryObject(int(name))
        return IUserProfile(profile, None)


@adapter_config(name='zmi_profile',
                required=(Interface, Interface),
                provides=ITALESExtension)
class UserProfileExtension(ContextRequestAdapter):
    """zmi_profile TALES extension"""

    def render(self, request=None):
        if request is None:
            request = self.request
        return IUserProfile(request)
