# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2016 Dariusz Suchojad <dsuch at zato.io>
Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
https://zato.io
"""

# stdlib
from unittest import TestCase

# six
from six import PY2

# Zato
from zato.elem import Elem
from zato.elem._serial import DictSerializer

# ################################################################################################################################

class Serial(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_on_list_child_idx_error_eq_0(self):

        elem = Elem()
        elem.a[0] = 'a0'
        elem.a[1] = 'a1'
        name = 'a'
        out = {}

        ds = DictSerializer()

        try:
            ds.on_list_child(1, name, elem, out)
        except ValueError as e:
            self.assertTrue(e.args[0].startswith('Unexpected input (first), idx:`1`, name:`a`, elem:`<Elem at '))
            self.assertTrue(e.args[0].endswith('>`, out:`{}`'))

    def test_on_list_child_idx_error_gt_0(self):

        elem = Elem()
        elem.a[0] = 'a0'
        elem.a[1] = 'a1'
        name = 'a'
        out = {'a':['a0', 'a1']}

        ds = DictSerializer()

        try:
            ds.on_list_child(3, name, elem, out)
        except ValueError as e:
            self.assertTrue(e.args[0].startswith('Unexpected input (append), idx:`3`, name:`a`, elem:`<Elem at '))
            self.assertTrue(e.args[0].endswith(">`, out:`{u'a': [u'a0', u'a1']}`" if PY2 else ">`, out:`{'a': ['a0', 'a1']}`"))
