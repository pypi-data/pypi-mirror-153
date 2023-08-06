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

"""PyAMS_zmi.interfaces.configuration module

This module defines interfaces of ZMI configuration.
"""

from collections import OrderedDict

from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, List, TextLine
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from myams_js import darkmode_core_bundle, darkmode_core_svg_bundle, darkmode_full_bundle, \
    darkmode_mini_bundle, \
    darkmode_mini_svg_bundle, \
    emerald_core_bundle, emerald_core_svg_bundle, emerald_full_bundle, emerald_mini_bundle, \
    emerald_mini_svg_bundle, \
    myams_core_bundle, myams_core_svg_bundle, \
    myams_full_bundle, myams_mini_bundle, myams_mini_svg_bundle
from pyams_file.schema import FileField, ImageField
from pyams_i18n.schema import I18nTextLineField


__docformat__ = 'restructuredtext'

from pyams_zmi import _


MYAMS_BUNDLES = OrderedDict((
    ('full', (myams_full_bundle, _("MyAMS full bundle"))),
    ('mini', (myams_mini_bundle, _("MyAMS mini bundle (with CSS icons)"))),
    ('mini-svg', (myams_mini_svg_bundle, _("MyAMS mini bundle (with SVG icons)"))),
    ('core', (myams_core_bundle, _("MyAMS core bundle (with CSS icons)"))),
    ('core-svg', (myams_core_svg_bundle, _("MyAMS core bundle (with SVG icons)"))),
    ('emerald', (emerald_full_bundle, _("Emerald full bundle"))),
    ('emerald-mini', (emerald_mini_bundle, _("Emerald mini bundle (with CSS icons)"))),
    ('emerald-mini-svg', (emerald_mini_svg_bundle, _("Emerald mini bundle (with SVG icons)"))),
    ('emerald-core', (emerald_core_bundle, _("Emerald core bundle (with CSS icons)"))),
    ('emerald-core-svg', (emerald_core_svg_bundle, _("Emerald core bundle (with SVG icons)"))),
    ('darkmode', (darkmode_full_bundle, _("Dark mode full bundle"))),
    ('darkmode-mini', (darkmode_mini_bundle, _("Dark mode mini bundle (with CSS icons)"))),
    ('darkmode-mini-svg', (darkmode_mini_svg_bundle, _("Dark mode mini bundle (with SVG icons)"))),
    ('darkmode-core', (darkmode_core_bundle, _("Dark mode core bundle (with CSS icons)"))),
    ('darkmode-core-svg', (darkmode_core_svg_bundle, _("Dark mode core bundle (with SVG icons)")))
))

MYAMS_BUNDLES_VOCABULARY = SimpleVocabulary(
    [SimpleTerm(k, title=v[1]) for k, v in MYAMS_BUNDLES.items()])

USER_BUNDLES_VOCABULARY = 'pyams_zmi.profile.bundles'


class IZMIConfiguration(Interface):
    """Static management configuration interface"""

    site_name = TextLine(title=_("Site name"),
                         default='PyAMS website',
                         required=False)

    home_name = I18nTextLineField(title=_("Home name"),
                                  description=_("Label used to get access to site's root in "
                                                "breadcrumbs link"),
                                  required=False)

    application_name = TextLine(title=_("Application name"),
                                default='PyAMS',
                                required=False)

    application_package = TextLine(title=_("Application package"),
                                   description=_("Name of the main package used to get "
                                                 "application version"),
                                   default='pyams_zmi',
                                   required=False)

    inner_package_name = TextLine(title=_("Secondary name"),
                                  required=False)

    inner_package = TextLine(title=_("Secondary package"),
                             description=_("Name of the secondary package used to complete "
                                           "application version"),
                             required=False)

    environment = TextLine(title=_("Environment name"),
                           description=_("Short text used to describe runtime environment"),
                           required=False)

    version = Attribute("Application version")

    myams_bundle = Choice(title=_("MyAMS bundle"),
                          description=_("MyAMS bundle used by the application"),
                          vocabulary=MYAMS_BUNDLES_VOCABULARY,
                          default='full')

    user_bundle_selection = Bool(title=_("Allow bundle selection from user profile"),
                                 description=_("If 'yes', bundle and theme selections "
                                               "will be available from user profile"),
                                 required=True,
                                 default=False)

    user_bundles = List(title=_("User selected bundles"),
                        description=_("List of bundles which can be selected from "
                                      "user profile"),
                        value_type=Choice(vocabulary=MYAMS_BUNDLES_VOCABULARY),
                        required=False)

    favicon = ImageField(title=_("Icon"),
                         description=_("Favorites icon"),
                         required=False)

    include_header = Bool(title=_("Include header"),
                          required=False,
                          default=True)

    fixed_header = Bool(title=_("Fixed header"),
                        description=_("If selected, the header will not scroll but will stay "
                                      "fixed at the top of the screen"),
                        required=False,
                        default=True)

    logo = ImageField(title=_("Logo image"),
                      description=_("SVG or bitmap image used as logo"),
                      required=False)

    include_site_search = Bool(title=_("Include site search"),
                               description=_("Include a global site search access link "
                                             "in page header"),
                               required=False,
                               default=False)

    site_search_placeholder = I18nTextLineField(title=_("Site search placeholder"),
                                                required=False)

    site_search_handler = TextLine(title=_("Site search handler"),
                                   required=False,
                                   default='#search.html')

    include_menus = Bool(title=_("Include navigation menus"),
                         required=False,
                         default=True)

    include_minify_button = Bool(title=_("Include minify buttons"),
                                 description=_("If selected, this will provide features to "
                                               "reduce or hide navigation menus"),
                                 required=True,
                                 default=True)

    fixed_navigation = Bool(title=_("Fixed menus"),
                            required=True,
                            default=False)

    accordion_menus = Bool(title=_("Accordion menus"),
                           description=_("If selected, only one navigation menu can be opened "
                                         "at a given time"),
                           required=True,
                           default=True)

    include_ribbon = Bool(title=_("Include ribbon"),
                          description=_("Display breadcrumbs ribbon?"),
                          required=False,
                          default=True)

    fixed_ribbon = Bool(title=_("Fixed ribon"),
                        description=_("If selected, the ribbon will not scroll but will stay "
                                      "fixed at the top of the page"),
                        required=True,
                        default=True)

    base_body_css_class = TextLine(title=_("Base body CSS class"),
                                   required=False)

    body_css_class = Attribute("HTML body CSS class")

    custom_stylesheet = FileField(title=_("Custom stylesheet"),
                                  description=_("Custom stylesheet used to override or extend "
                                                "default MyAMS management skin"),
                                  required=False)

    custom_script = FileField(title=_("Custom script"),
                              description=_("Custom javascript used to override or extend "
                                            "default MyAMS modules"),
                              required=False)
