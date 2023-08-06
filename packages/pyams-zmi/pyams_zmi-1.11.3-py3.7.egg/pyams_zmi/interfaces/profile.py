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

"""PyAMS_zmi.interfaces.profile module

This module defines the interfaces which are required to handle ZMI-related settings
in user profile.
"""

from zope.annotation import IAttributeAnnotatable
from zope.schema import Choice

from pyams_file.schema import ThumbnailImageField


__docformat__ = 'restructuredtext'

from pyams_zmi import _
from pyams_zmi.interfaces.configuration import USER_BUNDLES_VOCABULARY


USER_PROFILE_KEY = 'pyams_zmi.profile'


class IUserProfile(IAttributeAnnotatable):
    """User public profile preferences"""

    avatar = ThumbnailImageField(title=_("Profile's avatar"),
                                 description=_("This picture will be associated to your user "
                                               "profile"),
                                 required=False)

    zmi_bundle = Choice(title=_("Graphical theme"),
                        description=_("You can choose a custom theme between those "
                                      "provided in this selection list"),
                        vocabulary=USER_BUNDLES_VOCABULARY,
                        required=False)

    def get_avatar(self, selection='square', size='48x48'):
        """Get URL of avatar thumbnail for given selection and size"""
