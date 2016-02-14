# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>
Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
https://zato.io
"""

# stdlib
from unittest import TestCase

# Zato
from .common import rand_string
from zato.elem._common import Attr, Elem, NSInfo
from zato.elem._json import json
from zato.elem._xml import xml

# ################################################################################################################################

class StrRepr(TestCase):
    """ Tests __str__ and __repr__ methods.
    """
    def test_attr(self):
        name, value, ns_prefix, ns = rand_string(4)
        ns_prefix = ns_prefix[:5]
        ns_map = {ns_prefix: ns}

        self.assertRegexpMatches(
            repr(Attr(name, value, ns, ns_map)),
            '<Attr at 0x\w+ name:`{}` value:`{}`>'.format(name[1:], value))

# ################################################################################################################################

    def test_ns_info(self):
        value, ns_key, ns_value = rand_string(3)
        ns_map = {ns_key:ns_value}

        self.assertRegexpMatches(
            str(NSInfo(value, ns_map)), "<NSInfo at 0x\w+ prefix:`` value:`{}` is_def:`0` map:`{{'{}': '{}'}}`>".format(
                value, ns_key, ns_value))

# ################################################################################################################################

    def test_elem_has_value(self):
        doc = Elem()
        doc.ns_map = {'x':'example.com', 'q':'example.com/2'}

        value = rand_string()
        doc.a.b.x_c.d.e.q_f.x_g.h.q_j = value

        self.assertRegexpMatches(
            repr(doc.a.b.x_c.d.e.q_f.x_g.h.q_j), '<Elem at 0x\w+ a.b.x:c.d.e.q:f.x:g.h.q:j `{}`>'.format(value))

# ################################################################################################################################

    def test_elem_no_value(self):
        doc = Elem()
        doc.ns_map = {'x':'example.com', 'q':'example.com/2'}
        doc.a.b.x_c.d.e.q_f.x_g.h.q_j # No value

        self.assertRegexpMatches(repr(doc.a.b.x_c.d.e.q_f.x_g.h.q_j), '<Elem at 0x\w+ a.b.x:c.d.e.q:f.x:g.h.q:j>')

# ################################################################################################################################

    def test_json_has_value(self):
        doc = json()
        doc.ns_map = {'x':'example.com', 'q':'example.com/2'}

        value = rand_string()
        doc.a.b.x_c.d.e.q_f.x_g.h.q_j = value

        self.assertRegexpMatches(
            repr(doc.a.b.x_c.d.e.q_f.x_g.h.q_j),
            '<json at 0x\w+ a.b.x:c.d.e.q:f.x:g.h.q:j `{}`>'.format(value))

# ################################################################################################################################

    def test_json_no_value(self):
        doc = json()
        doc.ns_map = {'x':'example.com', 'q':'example.com/2'}
        doc.a.b.x_c.d.e.q_f.x_g.h.q_j # No value

        self.assertRegexpMatches(repr(doc.a.b.x_c.d.e.q_f.x_g.h.q_j), '<json at 0x\w+ a.b.x:c.d.e.q:f.x:g.h.q:j>')

# ################################################################################################################################

    def test_xml_has_value(self):
        doc = xml()
        doc.ns_map = {'x':'example.com', 'q':'example.com/2'}

        value = rand_string()
        doc.a.b.x_c.d.e.q_f.x_g.h.q_j = value

        self.assertRegexpMatches(
            repr(doc.a.b.x_c.d.e.q_f.x_g.h.q_j),
            '<xml at 0x\w+ /a/b/x:c/d/e/q:f/x:g/h/q:j `{}`>'.format(value))

# ################################################################################################################################

    def test_xml_no_value(self):
        doc = xml()
        doc.ns_map = {'x':'example.com', 'q':'example.com/2'}
        doc.a.b.x_c.d.e.q_f.x_g.h.q_j # No value

        self.assertRegexpMatches(repr(doc.a.b.x_c.d.e.q_f.x_g.h.q_j), '<xml at 0x\w+ /a/b/x:c/d/e/q:f/x:g/h/q:j>')

# ################################################################################################################################
