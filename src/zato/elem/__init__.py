# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>
Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
https://zato.io
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from doctest import Example

# lxml
from lxml.doctestcompare import LXMLOutputChecker, NOPARSE_MARKUP, PARSE_XML

# Zato
from ._common import default_ns, Elem, no_value
from ._json import json
from ._util import bunchify
from ._xml import xml

# For flake8
bunchify = bunchify
default_ns = default_ns
Elem = Elem
json = json
NOPARSE_MARKUP = NOPARSE_MARKUP
no_value = no_value
xml = xml

def compare_xml(expected, given, diff_format=PARSE_XML):
    checker = LXMLOutputChecker()
    if not checker.check_output(expected.strip(), given.strip(), PARSE_XML):
        raise AssertionError(checker.output_difference(Example('', expected), given.decode('utf8'), diff_format))
