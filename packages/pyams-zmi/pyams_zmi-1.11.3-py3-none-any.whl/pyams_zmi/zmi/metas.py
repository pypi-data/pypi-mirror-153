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

"""PyAMS_zmi.zmi.metas module

Custom management interface metas headers.
"""

__docformat__ = 'restructuredtext'

from datetime import datetime

from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface

from pyams_file.skin.view import FileView
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.interfaces.metas import IHTMLContentMetas
from pyams_skin.metas import LinkMeta
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.request import copy_request
from pyams_utils.timezone import tztime
from pyams_utils.url import absolute_url
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.configuration import IZMIConfiguration


THUMB_HREF_STR = '{}/++thumb++{}x{}?_={}'


@adapter_config(name='favicon',
                required=(Interface, IAdminLayer, Interface),
                provides=IHTMLContentMetas)
class IconMetasAdapter(ContextRequestViewAdapter):
    """Icon metas adapter"""

    weight = 20

    def get_metas(self):
        """Metas getter"""
        config = IZMIConfiguration(self.request.root, None)
        if (config is not None) and (config.favicon is not None):
            icon = config.favicon
            icon_url = absolute_url(icon, self.request)
            icon_size = icon.get_image_size()[0]  # pylint: disable=no-member
            dc = IZopeDublinCore(icon)  # pylint: disable=invalid-name
            timestamp = datetime.timestamp(tztime(dc.modified))
            for size in (180, 144, 114, 72, 32, 16):
                if icon_size >= size:
                    yield LinkMeta('apple-touch-icon',
                                   type=icon.content_type,  # pylint: disable=no-member
                                   href=THUMB_HREF_STR.format(icon_url, size, size, timestamp),
                                   sizes='{0}x{0}'.format(size))
            for size in (128, 124, 32):
                if icon_size >= size:
                    yield LinkMeta('icon',
                                   type=icon.content_type,  # pylint: disable=no-member
                                   href=THUMB_HREF_STR.format(icon_url, size, size, timestamp),
                                   sizes='{0}x{0}'.format(size))
            yield LinkMeta('shortcut-icon', type=icon.content_type, href=icon_url)  # pylint: disable=no-member


@view_config(name='favicon.ico', request_type=IPyAMSLayer)
def favorite_icon(request):
    """Favorite icon view"""
    configuration = IZMIConfiguration(request.context)
    if configuration.favicon is not None:
        request = copy_request(request)
        request.context = configuration.favicon
        return FileView(request)
    return HTTPNotFound()
