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
from zato.elem import compare_xml, NOPARSE_MARKUP, xml

# ################################################################################################################################

class Compare(TestCase):
    """ Tests how comparisons works.
    """
    def test_ok(self):
        orig = """
        <root>
          <a>
            <b>ccc</b>
          </a>
        </root>
        """
        doc = xml()
        doc.root.a.b = 'ccc'
        compare_xml(orig, doc.to_xml())

# ################################################################################################################################

    def test_ok_ns_default(self):
        orig = """
        <root xmlns="example.com">
          <a>
            <b>ccc</b>
          </a>
        </root>
        """
        doc = xml()
        doc.ns = 'example.com'
        doc.root.a.b = 'ccc'
        compare_xml(orig, doc.to_xml())

# ################################################################################################################################

    def test_ok_ns_custom(self):
        orig = """
        <root xmlns:x="example.com" xmlns:q="example.com/2">
          <x:a>
            <q:b>ccc</q:b>
          </x:a>
        </root>
        """
        doc = xml()
        doc.ns_map += {'x':'example.com', 'q':'example.com/2'}
        doc.root.x_a.q_b = 'ccc'
        compare_xml(orig, doc.to_xml())

# ################################################################################################################################

    def test_diff_parse_xml(self):
        orig = """
        <root>
          <a>
            <b>ccc</b>
          </a>
        </root>
        """
        doc = xml()
        doc.root.a.b.ddd = 'eee'

        expected = """
Expected:
  <root>
    <a>
      <b>ccc</b>
    </a>
  </root>

Got:
  <root>
    <a>
      <b>
        <ddd>eee</ddd>
      </b>
    </a>
  </root>

Diff:
  <root>
    <a>
      <b>
      ccc (got: None)
        +<ddd>eee</ddd>
      </b>
    </a>
  </root>
        """

        try:
            compare_xml(orig, doc.to_xml())
        except AssertionError as e:
            self.assertEquals(e.args[0].strip(), expected.strip())

# ################################################################################################################################

    def test_diff_noparse_markup(self):
        orig = """
        <root>
          <a>
            <b>ccc</b>
          </a>
        </root>
        """
        doc = xml()
        doc.root.a.b.ddd = 'eee'

        expected = """
Expected:

            <root>
              <a>
                <b>ccc</b>
              </a>
            </root>
            
Got:
    <root><a><b><ddd>eee</ddd></b></a></root>
        """

        try:
            compare_xml(orig, doc.to_xml(), NOPARSE_MARKUP)
        except AssertionError as e:
            self.assertEquals(e.args[0].strip(), expected.strip())

# ################################################################################################################################
