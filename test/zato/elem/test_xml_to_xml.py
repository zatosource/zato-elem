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

# lxml
from lxml.etree import _Element, tostring

# Zato
from zato.elem import compare_xml, xml

# ################################################################################################################################

class ToXML(TestCase):
    """ Tests how to_xml method works.
    """
    def setUp(self):
        self.maxDiff = None

    def test_to_xml_defaults(self):
        orig = """
        <root xmlns="example.com">
          <aaa>111</aaa>
        </root>
        """
        doc = xml()
        doc.root.ns = 'example.com'
        doc.root.aaa = '111'
        compare_xml(orig, doc.to_xml())

# ################################################################################################################################

    def test_to_xml_no_root(self):
        doc = xml()
        try:
            doc.to_xml()
        except ValueError as e:
            self.assertEquals(e.args[0], 'No root node found')
        else:
            self.fail('No root yet no ValueError raised')

# ################################################################################################################################

    def test_to_xml_multiple_roots(self):
        doc = xml()
        doc.aaa = '123'
        doc.bbb = '456'
        try:
            doc.to_xml()
        except ValueError as e:
            self.assertRegexpMatches(
                e.args[0],
                r'Multiple roots found: `\[<xml at 0x\w+ /aaa `123`>, <xml at 0x\w+ /bbb `456`>\]`')
        else:
            self.fail('Multiple roots yet no ValueError raised')

# ################################################################################################################################

    def test_to_xml_serialize_non_root(self):
        expected = """
        <d>
          <e>
            <f>111</f>
          </e>
        </d>
        """
        doc = xml()
        doc.a.b.c.d.e.f = '111'
        compare_xml(expected, doc.a.b.c.d.to_xml())

# ################################################################################################################################

    def test_to_xml_to_lxml(self):
        orig = """
            <root xmlns="example.com">
              <aaa>111</aaa>
            </root>
            """
        doc = xml()
        doc.root.ns = 'example.com'
        doc.root.aaa = '111'

        result = doc.to_xml(False)
        self.assertIsInstance(result, _Element)

        compare_xml(orig, tostring(result))

# ################################################################################################################################

    def test_to_xml_to_lxml_cleanup_ns_true(self):
        orig = """
              <root>
              <a xmlns:x="bar/x">
                <x:b foo="bar/foo1">
                    <x:ccc xmlns:rep="bar/rep">111</x:ccc>
                </x:b>
                <x:b foo="bar/foo2"/>
              </a>
            </root>
      """
        doc = xml()
        doc.ns_map += {'x':'bar/x', 'rep':'bar/rep'}

        root = doc.root
        b = root.a.x_b[0]
        b._foo = 'bar/foo1'
        b.x_ccc = '111'
        root.a.x_b[1]._foo = 'bar/foo2'

        expected = b'<root xmlns:x="bar/x"><a><x:b foo="bar/foo1"><x:ccc>111</x:ccc></x:b><x:b foo="bar/foo2"/></a></root>'
        result = doc.to_xml()

        # Compare
        compare_xml(orig, result)

        # Now, we expect for our namespace to be defined as in 'result', i.e. each namespace is declared once
        self.assertEquals(expected, result)

# ################################################################################################################################

    def test_to_xml_to_lxml_cleanup_ns_false(self):
        orig = """
              <root>
              <a xmlns:x="bar/x">
                <x:b foo="bar/foo1">
                    <x:ccc xmlns:rep="bar/rep">111</x:ccc>
                </x:b>
                <x:b foo="bar/foo2"/>
              </a>
            </root>
      """
        doc = xml()
        doc.ns_map += {'x':'bar/x', 'rep':'bar/rep'}

        root = doc.root
        b = root.a.x_b[0]
        b._foo = 'bar/foo1'
        b.x_ccc = '111'
        root.a.x_b[1]._foo = 'bar/foo2'

        expected = b'<root><a><ns0:b xmlns:ns0="bar/x" foo="bar/foo1"><ns0:ccc>111</ns0:ccc></ns0:b><ns1:b xmlns:ns1="bar/x"\
 foo="bar/foo2"/></a></root>'
        result = doc.to_xml(cleanup_ns=False)

        # Compare
        compare_xml(orig, result)

        # Here lxml assigned its own namespace prefixes
        self.assertEquals(expected, result)

# ################################################################################################################################
