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

"""PyAMS_zmi.helper.container module

This module provides container-related helpers to delete elements or update elements
attributes.
"""

from pyramid.httpexceptions import HTTPForbidden, HTTPInternalServerError

from pyams_security.permission import get_edit_permission


__docformat__ = 'restructuredtext'

from pyams_skin import _


def delete_container_element(request, container_factory=None, ignore_permission=False):
    """Delete container element

    This view is not strictly protected, but:
    - either the function is called from another protected view
    - either the view is checking edit permission from context adapter; if permission can't be
      found, an internal server error is raised!
    If the function is called from another unprotected view with 'ignore_permission=True',
    it's a configuration error.

    :param request: the current request
    :param container_factory: adapter interface or factory which may be used to access required
        container values
    :param ignore_permission: if False, container's edit permission is checked and an exception is
        raised if request doesn't have required permission; otherwise, no permission is checked.
        This argument should be set to True only when the function is called from another view
        which already checked required permission.
    """
    translate = request.localizer.translate
    # Get object name to be removed
    name = request.params.get('object_name')
    if not name:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("No provided object_name argument!"))
            }
        }
    # Check container factory
    container = request.context
    if container_factory is not None:
        container = container_factory(container)
    # Check container
    if name not in container:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("Given element name doesn't exist!"))
            }
        }
    # Check permission
    context = container[name]
    if not ignore_permission:
        permission = get_edit_permission(request, context, action='delete')
        if permission is None:
            raise HTTPInternalServerError("Missing permission definition!")
        if not request.has_permission(permission, context=context):
            raise HTTPForbidden()
    # Delete element
    del container[name]
    return {
        'status': 'success',
        'message': translate(_("Element was deleted successfully."))
    }


def switch_element_attribute(request, container_factory=None, ignore_permission=False):
    """Switch attribute of a container element

    This view is not strictly protected, but:
    - either the function is called from another protected view
    - either the view is checking edit permission from context adapter; if permission can't be
      found, an internal server error is raised!
    If the function is called from another unprotected view with 'ignore_permission=True',
    it's a configuration error.

    :param request: the current request
    :param container_factory: adapter interface or factory which may be used to access required
        container values
    :param ignore_permission: if False, container's edit permission is checked and an exception is
        raised if request doesn't have required permission; otherwise, no permission is checked.
        This argument should be set to True only when the function is called from another view
        which already checked required permission.
    """
    translate = request.localizer.translate
    # Get object name to be removed
    name = request.params.get('object_name')
    if not name:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("No provided object_name argument!"))
            }
        }
    attribute = request.params.get('attribute_name')
    if not attribute:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("No provided attribute name!"))
            }
        }
    # Check container factory
    container = request.context
    if container_factory is not None:
        container = container_factory(container)
    # Check container
    if name not in container:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("Given element name doesn't exist!"))
            }
        }
    # Check permission
    context = container[name]
    if not ignore_permission:
        permission = get_edit_permission(request, context)
        if permission is None:
            raise HTTPInternalServerError("Missing permission definition!")
        if not request.has_permission(permission, context=context):
            raise HTTPForbidden()
    # Update element
    setattr(context, attribute, not getattr(context, attribute))
    return {
        'status': 'success',
        'message': translate(_("Element was updated successfully.")),
        'state': getattr(context, attribute)
    }
