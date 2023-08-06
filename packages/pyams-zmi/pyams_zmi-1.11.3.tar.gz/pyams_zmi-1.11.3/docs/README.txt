=================
PyAMS_zmi package
=================

.. contents::


What is PyAMS?
==============

PyAMS (Pyramid Application Management Suite) is a small suite of packages written for applications
and content management with the Pyramid framework.

**PyAMS** is actually mainly used to manage web sites through content management applications (CMS,
see PyAMS_content package), but many features are generic and can be used inside any kind of web
application.

All PyAMS documentation is available on `ReadTheDocs <https://pyams.readthedocs.io>`_; source code
is available on `Gitlab <https://gitlab.com/pyams>`_ and pushed to `Github
<https://github.com/py-ams>`_.


What is PyAMS_zmi?
==================

PyAMS_zmi is the base package which provides PyAMS user management interface; it's name is based
on the old Zope Management Interface, but the current implementation is based on the MyAMS
package.

This package is using many content providers and viewlet managers (including in forms), so it can
be extended easily by extensions packages without having to modify existing code.
