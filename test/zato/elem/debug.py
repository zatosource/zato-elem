# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Part of Zato - Open-source ESB, SOA, REST, APIs and Cloud Integrations in Python
# https://zato.io

from zato.elem import xml

doc = xml()
doc.root.ns = 'example.com'
doc.root.ns_map += {'x':'example.com/x'}
doc.root.x_a.b = '123'

doc.to_xml()
