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
from zato.elem import Elem, xml

# ################################################################################################################################

class Append(TestCase):
    """ Tests Elem.append.
    """
    def test_append_to_list1(self):
        doc = Elem()
        doc.a.append(123)

        expected = {'a': [123]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def test_append_to_list2(self):
        doc = Elem()
        doc.a[0] = 0
        doc.a.append(123)

        expected = {'a': [0, 123]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def test_append_to_list3(self):
        doc = Elem()
        doc.a[0] = 0
        doc.a[1] = 1
        doc.a.append(123)

        expected = {'a': [0, 1, 123]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def test_append_to_list4(self):
        doc = Elem()
        doc.a.append(123)
        doc.a.append(456)

        expected = {'a': [123, 456]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def test_append_to_list5(self):
        doc = Elem()
        doc.a.append(123)
        doc.a.append(456)
        doc.a[2] = 789

        expected = {'a': [123, 456, 789]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def test_append_to_list6(self):
        doc = Elem()
        doc.a[0] = 123
        doc.a.append(456)
        doc.a[2] = 789

        expected = {'a': [123, 456, 789]}
        out = doc.to_dict()

        self.assertDictEqual(expected, out)

# ################################################################################################################################

class AppendNS(TestCase):
    """ Tests Elem.append with namespaces.
    """

    def test_append_to_list1(self):

        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}
        doc.ns0_a[0] = 123

        expected = {'ns0_a': [123]}
        out = doc.to_dict(include_ns=True)

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def test_append_to_list2(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a[0] = 0
        doc.ns0_a.append(123)

        expected = {'ns0_a': [0, 123]}
        out = doc.to_dict(include_ns=True)

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def test_append_to_list3(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a[0] = 0
        doc.ns0_a[1] = 1
        doc.ns0_a.append(123)

        expected = {'ns0_a': [0, 1, 123]}
        out = doc.to_dict(include_ns=True)

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def test_append_to_list4(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a.append(123)
        doc.ns0_a.append(456)

        expected = {'ns0_a': [123, 456]}
        out = doc.to_dict(include_ns=True)

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def test_append_to_list5(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a.append(123)
        doc.ns0_a.append(456)
        doc.ns0_a[2] = 789

        expected = {'ns0_a': [123, 456, 789]}
        out = doc.to_dict(include_ns=True)

        self.assertDictEqual(expected, out)

# ################################################################################################################################

    def test_append_to_list6(self):
        doc = Elem()
        doc.ns_map += {'ns0':'example.com'}

        doc.ns0_a[0] = 123
        doc.ns0_a.append(456)
        doc.ns0_a[2] = 789

        expected = {'ns0_a': [123, 456, 789]}
        out = doc.to_dict(include_ns=True)

        self.assertDictEqual(expected, out)

# ################################################################################################################################
