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
from zato.elem import Elem

# ################################################################################################################################

class Contains(TestCase):
    """ Tests how __contains__ works.
    """

# ################################################################################################################################

    def test_contains_elem_no_ns(self):
        doc = Elem()
        doc.a.b.c = '123'

        doc2 = Elem()
        doc2.zz.qq.c = '456'
        doc2.zz.qq.d = '789'

        self.assertIn('c', doc.a.b)
        self.assertNotIn('d', doc.a.b)

        self.assertIn(doc2.zz.qq.c, doc.a.b)
        self.assertNotIn(doc2.zz.qq.d, doc.a.b)

# ################################################################################################################################

    def test_contains_elem_parent_ns(self):
        doc = Elem()
        doc.ns_map = {'ee':'example.com'}
        doc.a.b.ee_c = '123'

        # Has NS map
        doc2 = Elem()
        doc2.ns_map = {'ee':'example.com'}
        doc2.zz.qq.ee_c = '456'
        doc2.zz.qq.d = '789'

        # No NS map yet the prefix is the same
        doc3 = Elem()
        doc3.zz.qq.ee_c = '456'
        doc3.zz.qq.d = '789'

        self.assertIn('ee_c', doc.a.b)
        self.assertNotIn('c', doc.a.b)
        self.assertNotIn('ee_d', doc.a.b)

        self.assertIn(doc2.zz.qq.ee_c, doc.a.b)
        self.assertNotIn(doc2.zz.qq.ee_d, doc.a.b)

        self.assertIn(doc3.zz.qq.ee_c, doc.a.b)
        self.assertNotIn(doc3.zz.qq.ee_d, doc.a.b)

# ################################################################################################################################
