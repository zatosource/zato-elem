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
from zato.elem import compare_xml, xml

# ################################################################################################################################

class ListChildren(TestCase):
    """ Tests how list children are handled.
    """
    def test_ok(self):
        orig = """
        <aaa>
            <bbb>0</bbb>
            <bbb>1</bbb>
            <bbb>2</bbb>
            <bbb>3</bbb>
        </aaa>
        """
        doc = xml()
        doc.aaa.bbb[0] = '0'
        doc.aaa.bbb[1] = '1'
        doc.aaa.bbb[2] = '2'
        doc.aaa.bbb[3] = '3'

        compare_xml(orig, doc.to_xml())

# ################################################################################################################################

    def test_one_missing(self):
        """
        <aaa>
            <bbb>0</bbb>
            <bbb>1</bbb>
            <bbb>2</bbb>
            <bbb>3</bbb>
        </aaa>
        """
        doc = xml()
        doc.aaa.bbb[0] = '0'
        doc.aaa.bbb[1] = '1'

        try:
            doc.aaa.bbb[3] = '3'
        except IndexError as e:
            self.assertEquals(e.args[0], 'Cannot access idx 3, /aaa/bbb[2] is missing')
        else:
            self.fail('Expected IndexError not raised')

# ################################################################################################################################

    def test_multiple_missing(self):
        """
        <aaa>
            <bbb>0</bbb>
            <bbb>1</bbb>
            <bbb>2</bbb>
            <bbb>3</bbb>
            <bbb>4</bbb>
            <bbb>5</bbb>
        </aaa>
        """
        doc = xml()
        doc.aaa.bbb[0] = '0'
        doc.aaa.bbb[1] = '1'
        doc.aaa.bbb[2] = '2'

        try:
            doc.aaa.bbb[39] = '39'
        except IndexError as e:
            self.assertEquals(e.args[0], 'Cannot access idx 39, /aaa/bbb[3-38] are missing')
        else:
            self.fail('Expected IndexError not raised')

# ################################################################################################################################

    def test_one_missing_ns_default(self):
        """
        <aaa xmlns="example.com">
            <bbb>0</bbb>
            <bbb>1</bbb>
            <bbb>2</bbb>
            <bbb>3</bbb>
        </aaa>
        """
        doc = xml()
        doc.ns = 'example.com'
        doc.aaa.bbb[0] = '0'
        doc.aaa.bbb[1] = '1'

        try:
            doc.aaa.bbb[3] = '3'
        except IndexError as e:
            self.assertEquals(e.args[0], 'Cannot access idx 3, /aaa/bbb[2] is missing')
        else:
            self.fail('Expected IndexError not raised')

# ################################################################################################################################

    def test_multiple_missing_ns_default(self):
        """
        <aaa xmlns="example.com">
            <bbb>0</bbb>
            <bbb>1</bbb>
            <bbb>2</bbb>
            <bbb>3</bbb>
            <bbb>4</bbb>
            <bbb>5</bbb>
        </aaa>
        """
        doc = xml()
        doc.aaa.bbb[0] = '0'
        doc.aaa.bbb[1] = '1'
        doc.aaa.bbb[2] = '2'

        try:
            doc.aaa.bbb[39] = '39'
        except IndexError as e:
            self.assertEquals(e.args[0], 'Cannot access idx 39, /aaa/bbb[3-38] are missing')
        else:
            self.fail('Expected IndexError not raised')

# ################################################################################################################################

    def test_one_missing_ns_custom(self):
        """
        <z:aaa z:xmlns="example.com">
            <bbb>0</bbb>
            <bbb>1</bbb>
        </z:aaa>
        """
        doc = xml()
        doc.ns_map += {'z': 'example.com'}
        doc.z_aaa.bbb[0] = '0'
        doc.z_aaa.bbb[1] = '1'

        try:
            doc.z_aaa.bbb[3] = '3'
        except IndexError as e:
            self.assertEquals(e.args[0], 'Cannot access idx 3, /z:aaa/bbb[2] is missing')
        else:
            self.fail('Expected IndexError not raised')

# ################################################################################################################################

    def test_multiple_missing_ns_custom(self):
        """
        <aaa xmlns="example.com" xmlns:q="example.com">
            <q:bbb>0</q:bbb>
            <q:bbb>1</q:bbb>
            <q:bbb>2</q:bbb>
            <q:bbb>3</q:bbb>
            <q:bbb>4</q:bbb>
            <q:bbb>5</q:bbb>
        </aaa>
        """
        doc = xml()
        doc.ns_map += {'q': 'example.com'}
        doc.aaa.q_bbb[0] = '0'
        doc.aaa.q_bbb[1] = '1'
        doc.aaa.q_bbb[2] = '2'

        try:
            doc.aaa.q_bbb[39] = '39'
        except IndexError as e:
            self.assertEquals(e.args[0], 'Cannot access idx 39, /aaa/q:bbb[3-38] are missing')
        else:
            self.fail('Expected IndexError not raised')

# ################################################################################################################################
